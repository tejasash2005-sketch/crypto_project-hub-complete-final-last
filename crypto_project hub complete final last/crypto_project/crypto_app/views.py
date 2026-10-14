from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Count, Q
from django.utils import timezone
from django.views.decorators.http import require_POST
import json
import csv

from .models import (
    EncryptionLog, CryptoKey, FileEncryptionRecord, UserProfile,
    AlgorithmReference, QuizQuestion, QuizAttempt, ContactMessage,
    Announcement, ActivityLog, CommunicationMessage, BlockchainBlock,
    SteganographyRecord, ProfessionalSecurityRecord
)
from .professional_crypto import (
    prof_aes_encrypt, prof_aes_decrypt, prof_rsa_generate_keys,
    prof_rsa_sign, prof_rsa_verify, prof_ecc_generate, prof_ecc_sign,
    prof_totp_generate_secret, prof_totp_verify
)
from .forms import (
    CustomLoginForm, CustomRegisterForm, EncryptionForm,
    ContactForm, KeyGeneratorForm, ProfileUpdateForm, SendMessageForm
)
from .crypto_utils import (
    perform_encryption, generate_random_key, mine_new_block,
    encode_image_data, decode_image_data
)


def is_admin(user):
    return user.is_staff or user.is_superuser


def log_activity(user, action, description='', request=None, extra=None):
    ip = None
    ua = ''
    if request:
        ip = request.META.get('REMOTE_ADDR')
        ua = request.META.get('HTTP_USER_AGENT', '')
    ActivityLog.objects.create(
        user=user, action=action, description=description,
        ip_address=ip, user_agent=ua, extra_data=extra or {}
    )


# ============================================================
# PUBLIC PAGES (No login required)
# ============================================================
def home(request):
    """Public homepage with info about cryptography."""
    algorithms = AlgorithmReference.objects.filter(is_featured=True)[:6]
    announcements = Announcement.objects.filter(
        is_active=True, target_audience__in=['ALL']
    )[:3]
    stats = {
        'total_users': User.objects.count(),
        'total_encryptions': EncryptionLog.objects.count(),
        'algorithms_available': 11,
    }
    return render(request, 'crypto_app/home.html', {
        'algorithms': algorithms,
        'announcements': announcements,
        'stats': stats,
    })


def about(request):
    algorithms = AlgorithmReference.objects.all().order_by('category')
    return render(request, 'crypto_app/about.html', {'algorithms': algorithms})


def topics(request):
    algorithms = AlgorithmReference.objects.all().order_by('category')
    categories = AlgorithmReference.objects.values('category').distinct()
    return render(request, 'crypto_app/topics.html', {
        'algorithms': algorithms, 'categories': categories
    })


def topic_detail(request, pk):
    algorithm = get_object_or_404(AlgorithmReference, pk=pk)
    return render(request, 'crypto_app/topic_detail.html', {'algorithm': algorithm})


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            if request.user.is_authenticated:
                msg.user = request.user
            msg.save()
            messages.success(request, '✅ Your message has been sent! We will get back to you soon.')
            return redirect('contact')
    else:
        form = ContactForm()
        if request.user.is_authenticated:
            form.initial = {
                'name': request.user.get_full_name(),
                'email': request.user.email
            }
    return render(request, 'crypto_app/contact.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            log_activity(user, 'LOGIN', 'User logged in', request)
            if user.is_staff:
                return redirect('admin_dashboard')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = CustomLoginForm()
    return render(request, 'crypto_app/login.html', {'form': form})


def user_register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(
                user=user,
                expertise_level=form.cleaned_data.get('expertise_level', 'BEGINNER')
            )
            login(request, user)
            messages.success(request, f'Welcome, {user.first_name}! Your account is ready.')
            return redirect('dashboard')
    else:
        form = CustomRegisterForm()
    return render(request, 'crypto_app/register.html', {'form': form})


def user_logout(request):
    if request.user.is_authenticated:
        log_activity(request.user, 'LOGOUT', 'User logged out', request)
        logout(request)
    return redirect('home')


# ============================================================
# USER MODULES (Login required)
# ============================================================

# MODULE 1: Dashboard
@login_required
def dashboard(request):
    user = request.user
    profile, _ = UserProfile.objects.get_or_create(user=user)
    recent_logs = EncryptionLog.objects.filter(user=user)[:5]
    recent_keys = CryptoKey.objects.filter(user=user, is_active=True)[:3]
    announcements = Announcement.objects.filter(
        is_active=True, target_audience__in=['ALL', 'USERS']
    )[:3]
    stats = {
        'total_encryptions': EncryptionLog.objects.filter(user=user, operation='ENCRYPT').count(),
        'total_decryptions': EncryptionLog.objects.filter(user=user, operation='DECRYPT').count(),
        'saved_keys': CryptoKey.objects.filter(user=user, is_active=True).count(),
        'quiz_attempts': QuizAttempt.objects.filter(user=user).count(),
        'best_score': QuizAttempt.objects.filter(user=user).order_by('-percentage').first(),
        'unread_messages': CommunicationMessage.objects.filter(receiver=user, is_read=False).count(),
    }
    return render(request, 'crypto_app/dashboard.html', {
        'profile': profile,
        'recent_logs': recent_logs,
        'recent_keys': recent_keys,
        'announcements': announcements,
        'stats': stats,
    })


# MODULE 2: Encryption Tool
@login_required
def encryption_tool(request):
    result = None
    form = EncryptionForm()
    if request.method == 'POST':
        form = EncryptionForm(request.POST)
        if form.is_valid():
            algo = form.cleaned_data['algorithm']
            op = form.cleaned_data['operation']
            text = form.cleaned_data['input_text']
            key = form.cleaned_data['key']
            result = perform_encryption(algo, text, key, op)
            if form.cleaned_data.get('save_to_history', True):
                EncryptionLog.objects.create(
                    user=request.user,
                    algorithm=algo,
                    operation=op,
                    input_text=text[:500],
                    output_text=result.get('output', '')[:500],
                    key_used=result.get('key_used', '')[:200],
                    success=result.get('success', False)
                )
                profile, _ = UserProfile.objects.get_or_create(user=request.user)
                if op == 'ENCRYPT':
                    profile.total_encryptions += 1
                else:
                    profile.total_decryptions += 1
                profile.save()
            log_activity(request.user, op, f'{algo} operation performed', request)
    return render(request, 'crypto_app/encryption_tool.html', {'form': form, 'result': result})


# MODULE 3: Encryption History
@login_required
def encryption_history(request):
    logs = EncryptionLog.objects.filter(user=request.user)
    algo_filter = request.GET.get('algorithm', '')
    op_filter = request.GET.get('operation', '')
    if algo_filter:
        logs = logs.filter(algorithm=algo_filter)
    if op_filter:
        logs = logs.filter(operation=op_filter)
    return render(request, 'crypto_app/history.html', {
        'logs': logs,
        'algo_filter': algo_filter,
        'op_filter': op_filter,
    })


# MODULE 4: Key Manager
@login_required
def key_manager(request):
    keys = CryptoKey.objects.filter(user=request.user)
    form = KeyGeneratorForm()
    if request.method == 'POST':
        form = KeyGeneratorForm(request.POST)
        if form.is_valid():
            length = int(form.cleaned_data['length'])
            key_type = form.cleaned_data['key_type']
            generated = generate_random_key(length, key_type)
            CryptoKey.objects.create(
                user=request.user,
                name=form.cleaned_data['key_name'],
                key_type='SYMMETRIC',
                algorithm=form.cleaned_data['algorithm'],
                key_value=generated,
                description=form.cleaned_data.get('description', '')
            )
            log_activity(request.user, 'KEY_CREATE', f"Key '{form.cleaned_data['key_name']}' created", request)
            messages.success(request, '🔑 Key generated and saved successfully!')
            return redirect('key_manager')
    return render(request, 'crypto_app/key_manager.html', {'keys': keys, 'form': form})


@login_required
def delete_key(request, key_id):
    key = get_object_or_404(CryptoKey, id=key_id, user=request.user)
    key.is_active = False
    key.save()
    log_activity(request.user, 'KEY_DELETE', f"Key '{key.name}' deleted", request)
    messages.success(request, 'Key removed successfully.')
    return redirect('key_manager')


# MODULE 5: Algorithm Reference
@login_required
def algorithm_reference(request):
    algorithms = AlgorithmReference.objects.all()
    category = request.GET.get('category', '')
    if category:
        algorithms = algorithms.filter(category=category)
    return render(request, 'crypto_app/algorithm_reference.html', {
        'algorithms': algorithms, 'category': category
    })


# MODULE 6: Quiz Module
@login_required
def quiz_view(request):
    questions = list(QuizQuestion.objects.filter(is_active=True)[:10])
    if not questions:
        messages.warning(request, 'No quiz questions available yet.')
        return redirect('dashboard')
    return render(request, 'crypto_app/quiz.html', {'questions': questions})


@login_required
def quiz_submit(request):
    if request.method == 'POST':
        questions = QuizQuestion.objects.filter(is_active=True)[:10]
        score = 0
        results = []
        for q in questions:
            user_answer = request.POST.get(f'question_{q.id}', '')
            correct = user_answer == q.correct_answer
            if correct:
                score += 1
            results.append({
                'question': q.question,
                'user_answer': user_answer,
                'correct_answer': q.correct_answer,
                'correct': correct,
                'explanation': q.explanation
            })
        total = len(questions)
        pct = (score / total * 100) if total > 0 else 0
        attempt = QuizAttempt.objects.create(
            user=request.user, score=score,
            total_questions=total, percentage=pct
        )
        log_activity(request.user, 'QUIZ_ATTEMPT', f'Score: {score}/{total}', request)
        return render(request, 'crypto_app/quiz_result.html', {
            'score': score, 'total': total, 'percentage': pct,
            'results': results, 'attempt': attempt
        })
    return redirect('quiz')


# MODULE 7: Profile Management
@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            user = request.user
            user.first_name = form.cleaned_data.get('first_name', user.first_name)
            user.last_name = form.cleaned_data.get('last_name', user.last_name)
            user.email = form.cleaned_data.get('email', user.email)
            user.save()
            form.save()
            log_activity(request.user, 'PROFILE_UPDATE', 'Profile updated', request)
            messages.success(request, '✅ Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile, initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        })
    activity_logs = ActivityLog.objects.filter(user=request.user)[:10]
    quiz_attempts = QuizAttempt.objects.filter(user=request.user)[:5]
    return render(request, 'crypto_app/profile.html', {
        'profile': profile, 'form': form,
        'activity_logs': activity_logs, 'quiz_attempts': quiz_attempts
    })


# MODULE 10: Communication Module
@login_required
def inbox(request):
    messages_list = CommunicationMessage.objects.filter(receiver=request.user).order_by('-created_at')
    return render(request, 'crypto_app/communication/inbox.html', {'messages_list': messages_list})


@login_required
def sent_messages(request):
    messages_list = CommunicationMessage.objects.filter(sender=request.user).order_by('-created_at')
    return render(request, 'crypto_app/communication/sent.html', {'messages_list': messages_list})


@login_required
def send_message(request):
    if request.method == 'POST':
        form = SendMessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user

            # Encrypt the content before saving
            plain_text = form.cleaned_data['message_to_encrypt']
            algo = form.cleaned_data['algorithm']
            key = form.cleaned_data['encryption_key']

            result = perform_encryption(algo, plain_text, key, 'ENCRYPT')
            if result['success']:
                msg.encrypted_content = result['output']
                msg.save()
                messages.success(request, f'Message sent successfully to {msg.receiver.username}!')
                return redirect('sent_messages')
            else:
                messages.error(request, f"Encryption failed: {result['error']}")
    else:
        form = SendMessageForm()
    return render(request, 'crypto_app/communication/send_message.html', {'form': form})


@login_required
def view_message(request, pk):
    message = get_object_or_404(CommunicationMessage, pk=pk)
    if message.receiver != request.user and message.sender != request.user:
        messages.error(request, "Access denied.")
        return redirect('inbox')

    decrypted_content = None
    if request.method == 'POST' and message.receiver == request.user:
        key = request.POST.get('decryption_key')
        result = perform_encryption(message.algorithm, message.encrypted_content, key, 'DECRYPT')
        if result['success']:
            decrypted_content = result['output']
            if not message.is_read:
                message.is_read = True
                message.save()
        else:
            messages.error(request, "Decryption failed. Please check the key.")

    return render(request, 'crypto_app/communication/view_message.html', {
        'message': message,
        'decrypted_content': decrypted_content
    })


@login_required
def delete_message(request, pk):
    message = get_object_or_404(CommunicationMessage, pk=pk)
    if message.sender == request.user or message.receiver == request.user:
        message.delete()
        messages.success(request, 'Message deleted successfully.')
    else:
        messages.error(request, 'You do not have permission to delete this message.')

    # Redirect based on where the user might have come from
    referer = request.META.get('HTTP_REFERER', '')
    if 'inbox' in referer:
        return redirect('inbox')
    return redirect('sent_messages')


# MODULE 8: Announcements
@login_required
def announcements_view(request):
    announcements = Announcement.objects.filter(
        is_active=True, target_audience__in=['ALL', 'USERS']
    )
    return render(request, 'crypto_app/announcements.html', {'announcements': announcements})


# MODULE 9: Activity Log
@login_required
def activity_log(request):
    logs = ActivityLog.objects.filter(user=request.user)[:50]
    return render(request, 'crypto_app/activity_log.html', {'logs': logs})


# AJAX endpoint
@login_required
def ajax_encrypt(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        result = perform_encryption(
            data.get('algorithm', 'CAESAR'),
            data.get('text', ''),
            data.get('key', ''),
            data.get('operation', 'ENCRYPT')
        )
        return JsonResponse(result)
    return JsonResponse({'error': 'Invalid request'}, status=400)


# ============================================================
# ADMIN MODULES
# ============================================================

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    stats = {
        'total_users': User.objects.filter(is_staff=False).count(),
        'total_encryptions': EncryptionLog.objects.count(),
        'open_messages': ContactMessage.objects.filter(status='NEW').count(),
        'active_keys': CryptoKey.objects.filter(is_active=True).count(),
        'quiz_attempts': QuizAttempt.objects.count(),
        'algorithms': AlgorithmReference.objects.count(),
    }
    recent_users = User.objects.filter(is_staff=False).order_by('-date_joined')[:5]
    recent_logs = EncryptionLog.objects.select_related('user').order_by('-created_at')[:8]
    recent_messages = ContactMessage.objects.filter(status='NEW')[:5]
    return render(request, 'admin_panel/admin_dashboard.html', {
        'stats': stats,
        'recent_users': recent_users,
        'recent_logs': recent_logs,
        'recent_messages': recent_messages,
    })


# Admin MODULE 1: User Management
@login_required
@user_passes_test(is_admin)
def admin_users(request):
    users = User.objects.filter(is_staff=False).select_related('profile').order_by('-date_joined')
    search = request.GET.get('search', '')
    if search:
        users = users.filter(Q(username__icontains=search) | Q(email__icontains=search))
    return render(request, 'admin_panel/admin_users.html', {'users': users, 'search': search})


@login_required
@user_passes_test(is_admin)
def admin_toggle_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()
    status = 'activated' if user.is_active else 'deactivated'
    messages.success(request, f'User {user.username} has been {status}.')
    return redirect('admin_users')


# Admin MODULE 2: Encryption Logs
@login_required
@user_passes_test(is_admin)
def admin_logs(request):
    logs = EncryptionLog.objects.select_related('user').order_by('-created_at')
    user_filter = request.GET.get('user', '')
    algo_filter = request.GET.get('algorithm', '')
    if user_filter:
        logs = logs.filter(user__username__icontains=user_filter)
    if algo_filter:
        logs = logs.filter(algorithm=algo_filter)
    return render(request, 'admin_panel/admin_logs.html', {
        'logs': logs, 'user_filter': user_filter, 'algo_filter': algo_filter
    })


# Admin MODULE 3: Algorithm Manager
@login_required
@user_passes_test(is_admin)
def admin_algorithms(request):
    algorithms = AlgorithmReference.objects.all()
    if request.method == 'POST':
        AlgorithmReference.objects.create(
            name=request.POST.get('name'),
            acronym=request.POST.get('acronym'),
            category=request.POST.get('category'),
            description=request.POST.get('description'),
            how_it_works=request.POST.get('how_it_works', ''),
            use_cases=request.POST.get('use_cases', ''),
            complexity=request.POST.get('complexity', 'MEDIUM'),
            is_featured=request.POST.get('is_featured') == 'on'
        )
        messages.success(request, 'Algorithm added successfully!')
        return redirect('admin_algorithms')
    return render(request, 'admin_panel/admin_algorithms.html', {'algorithms': algorithms})


# Admin MODULE 4: Quiz Management
@login_required
@user_passes_test(is_admin)
def admin_quiz(request):
    questions = QuizQuestion.objects.all()
    attempts = QuizAttempt.objects.select_related('user').order_by('-attempted_at')[:20]
    if request.method == 'POST':
        QuizQuestion.objects.create(
            question=request.POST.get('question'),
            option_a=request.POST.get('option_a'),
            option_b=request.POST.get('option_b'),
            option_c=request.POST.get('option_c'),
            option_d=request.POST.get('option_d'),
            correct_answer=request.POST.get('correct_answer'),
            explanation=request.POST.get('explanation', ''),
            difficulty=request.POST.get('difficulty', 'MEDIUM'),
        )
        messages.success(request, 'Question added successfully!')
        return redirect('admin_quiz')
    return render(request, 'admin_panel/admin_quiz.html', {
        'questions': questions, 'attempts': attempts
    })


# Admin MODULE 5: Contact Messages
@login_required
@user_passes_test(is_admin)
def admin_messages(request):
    contact_messages = ContactMessage.objects.all().order_by('-created_at')
    status_filter = request.GET.get('status', '')
    if status_filter:
        contact_messages = contact_messages.filter(status=status_filter)
    return render(request, 'admin_panel/admin_messages.html', {
        'messages_list': contact_messages, 'status_filter': status_filter
    })


@login_required
@user_passes_test(is_admin)
def admin_reply_message(request, msg_id):
    msg = get_object_or_404(ContactMessage, id=msg_id)
    if request.method == 'POST':
        msg.admin_reply = request.POST.get('reply', '')
        msg.status = 'RESOLVED'
        msg.resolved_at = timezone.now()
        msg.save()
        messages.success(request, 'Reply saved and message marked as resolved.')
        return redirect('admin_messages')
    return render(request, 'admin_panel/admin_reply_message.html', {'msg': msg})


# Admin MODULE 6: Announcements
@login_required
@user_passes_test(is_admin)
def admin_announcements(request):
    announcements = Announcement.objects.all()
    if request.method == 'POST':
        Announcement.objects.create(
            title=request.POST.get('title'),
            content=request.POST.get('content'),
            priority=request.POST.get('priority', 'MEDIUM'),
            target_audience=request.POST.get('target_audience', 'ALL'),
            created_by=request.user,
            is_active=request.POST.get('is_active') == 'on'
        )
        messages.success(request, 'Announcement published!')
        return redirect('admin_announcements')
    return render(request, 'admin_panel/admin_announcements.html', {'announcements': announcements})


@login_required
@user_passes_test(is_admin)
def admin_toggle_announcement(request, ann_id):
    ann = get_object_or_404(Announcement, id=ann_id)
    ann.is_active = not ann.is_active
    ann.save()
    return redirect('admin_announcements')


# Admin MODULE 7: Key Management (all users)
@login_required
@user_passes_test(is_admin)
def admin_keys(request):
    keys = CryptoKey.objects.select_related('user').filter(is_active=True)
    return render(request, 'admin_panel/admin_keys.html', {'keys': keys})


# Admin MODULE 8: Activity Audit Trail
@login_required
@user_passes_test(is_admin)
def admin_activity(request):
    logs = ActivityLog.objects.select_related('user').order_by('-timestamp')[:100]
    return render(request, 'admin_panel/admin_activity.html', {'logs': logs})


# Admin MODULE 9: Reports & Analytics
@login_required
@user_passes_test(is_admin)
def admin_reports(request):
    algo_usage = EncryptionLog.objects.values('algorithm').annotate(count=Count('id')).order_by('-count')
    user_activity = User.objects.filter(is_staff=False).annotate(
        enc_count=Count('encryption_logs')
    ).order_by('-enc_count')[:10]
    daily_stats = EncryptionLog.objects.extra(
        select={'day': 'date(created_at)'}
    ).values('day').annotate(count=Count('id')).order_by('-day')[:7]
    return render(request, 'admin_panel/admin_reports.html', {
        'algo_usage': algo_usage,
        'user_activity': user_activity,
        'daily_stats': daily_stats,
    })


# ============================================================
# ADVANCED MODULE 11: Blockchain Explorer
# ============================================================
@login_required
def blockchain_view(request):
    blocks = BlockchainBlock.objects.filter(created_by=request.user).order_by('index')
    return render(request, 'crypto_app/blockchain.html', {'blocks': blocks})


@login_required
def mine_block_view(request):
    if request.method == 'POST':
        data = request.POST.get('data', 'Empty Block')
        last_block = BlockchainBlock.objects.filter(created_by=request.user).order_by('-index').first()

        if last_block:
            index = last_block.index + 1
            prev_hash = last_block.hash
        else:
            index = 0
            prev_hash = "0" * 64 # Genesis block

        nonce, hash_val, ts = mine_new_block(index, data, prev_hash)

        BlockchainBlock.objects.create(
            index=index,
            data=data,
            previous_hash=prev_hash,
            nonce=nonce,
            hash=hash_val,
            created_by=request.user
        )
        messages.success(request, f"🚀 Block #{index} successfully mined and added to the chain!")
        log_activity(request.user, 'BLOCKCHAIN_MINE', f"Mined block {index}", request)

    return redirect('blockchain')


# ============================================================
# ADVANCED MODULE 12: Steganography Module
# ============================================================
@login_required
def steganography_view(request):
    records = SteganographyRecord.objects.filter(user=request.user).order_by('-created_at')
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        text = request.POST.get('text', '')

        if text:
            from django.core.files.base import ContentFile
            output = encode_image_data(image, text)

            record = SteganographyRecord(user=request.user, original_image=image)
            record.stego_image.save(f"stego_{image.name}", ContentFile(output.read()), save=False)
            record.hidden_text = text[:100] + "..." # Store preview
            record.save()

            messages.success(request, "🎨 Message successfully hidden in image!")
            log_activity(request.user, 'STEGO_ENCODE', "Encoded message in image", request)
            return redirect('steganography')

    return render(request, 'crypto_app/steganography.html', {'records': records})


@login_required
def professional_suite(request):
    """Unified module for high-end professional security features."""
    results = None

    # Handle "View" from history
    view_id = request.GET.get('view_id')
    if view_id:
        record = get_object_or_404(ProfessionalSecurityRecord, id=view_id, user=request.user)
        if record.feature_type == 'RSA_PSS':
            results = {
                "type": "RSA-2048 Digital Signature (Stored)",
                "signature": record.output_data,
                "public_key": record.extra_info.get('pub'),
                "input": record.input_data
            }
        elif record.feature_type == 'AES_GCM':
            results = {
                "type": "AES-256-GCM Encryption (Stored)",
                "data": json.loads(record.output_data)
            }
        elif record.feature_type == 'ECC_EDDSA':
             results = {
                "type": "ECC (Ed25519) Identity (Stored)",
                "public_key": record.output_data,
                "private_key": "Redacted for security"
            }

    if request.method == 'POST':
        action = request.POST.get('action')
        input_text = request.POST.get('input_text', '')
        password = request.POST.get('password', 'default_pass')

        if action == 'AES_GCM_ENCRYPT':
            res = prof_aes_encrypt(input_text, password)
            results = {"type": "AES-256-GCM Encryption", "data": res}
            ProfessionalSecurityRecord.objects.create(
                user=request.user, feature_type='AES_GCM',
                input_data=input_text, output_data=json.dumps(res)
            )

        elif action == 'RSA_SIGN':
            priv, pub = prof_rsa_generate_keys()
            sig = prof_rsa_sign(input_text, priv)
            results = {
                "type": "RSA-2048 Digital Signature",
                "signature": sig,
                "public_key": pub,
                "private_key": priv,
                "input": input_text
            }
            ProfessionalSecurityRecord.objects.create(
                user=request.user, feature_type='RSA_PSS',
                input_data=input_text, output_data=sig,
                extra_info={"pub": pub, "priv": priv}
            )

        elif action == 'RSA_VERIFY':
            sig_to_check = request.POST.get('signature', '')
            pub_key = request.POST.get('public_key', '')
            is_valid = prof_rsa_verify(input_text, sig_to_check, pub_key)
            results = {
                "type": "Digital Signature Verification",
                "is_valid": is_valid,
                "message": "✅ Signature is VALID!" if is_valid else "❌ Signature is INVALID!"
            }

        elif action == 'ECC_GENERATE':
            priv, pub = prof_ecc_generate()
            results = {
                "type": "ECC (Ed25519) Key Pair",
                "public_key": pub,
                "private_key": priv
            }
            ProfessionalSecurityRecord.objects.create(
                user=request.user, feature_type='ECC_EDDSA',
                input_data="Key Generation", output_data=pub
            )

        elif action == 'TOTP_GEN':
            secret = prof_totp_generate_secret()
            results = {
                "type": "2FA (TOTP) Secret Generated",
                "secret": secret,
                "instruction": "Save this secret in your Authenticator App."
            }
            log_activity(request.user, 'PROFILE_UPDATE', 'Generated 2FA Secret')

        log_activity(request.user, 'ENCRYPT', f'Used Pro Suite: {action}')

    history = ProfessionalSecurityRecord.objects.filter(user=request.user)[:10]
    return render(request, 'crypto_app/professional_suite.html', {
        'results': results,
        'history': history
    })


@login_required
def steganography_decode(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        try:
            decoded_text = decode_image_data(image)
            if decoded_text:
                messages.info(request, f"🔍 Decoded Message: {decoded_text}")
            else:
                messages.warning(request, "No hidden message found or invalid format.")
        except Exception as e:
            messages.error(request, f"Decoding error: {str(e)}")

    return redirect('steganography')
