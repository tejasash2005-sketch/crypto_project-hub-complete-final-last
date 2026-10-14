from django.urls import path
from . import views

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('topics/', views.topics, name='topics'),
    path('topics/<int:pk>/', views.topic_detail, name='topic_detail'),
    path('contact/', views.contact_view, name='contact'),

    # Auth
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),

    # User Modules
    path('dashboard/', views.dashboard, name='dashboard'),
    path('encrypt/', views.encryption_tool, name='encryption_tool'),
    path('history/', views.encryption_history, name='history'),
    path('keys/', views.key_manager, name='key_manager'),
    path('keys/delete/<int:key_id>/', views.delete_key, name='delete_key'),
    path('algorithms/', views.algorithm_reference, name='algorithm_reference'),
    path('quiz/', views.quiz_view, name='quiz'),
    path('quiz/submit/', views.quiz_submit, name='quiz_submit'),
    path('profile/', views.profile_view, name='profile'),
    path('announcements/', views.announcements_view, name='announcements'),
    path('activity/', views.activity_log, name='activity_log'),
    path('ajax/encrypt/', views.ajax_encrypt, name='ajax_encrypt'),

    # Advanced Modules
    path('blockchain/', views.blockchain_view, name='blockchain'),
    path('blockchain/mine/', views.mine_block_view, name='mine_block'),
    path('steganography/', views.steganography_view, name='steganography'),
    path('steganography/decode/', views.steganography_decode, name='steganography_decode'),
    path('professional-suite/', views.professional_suite, name='professional_suite'),

    # Communication Module
    path('communication/inbox/', views.inbox, name='inbox'),
    path('communication/sent/', views.sent_messages, name='sent_messages'),
    path('communication/send/', views.send_message, name='send_message'),
    path('communication/view/<int:pk>/', views.view_message, name='view_message'),
    path('communication/delete/<int:pk>/', views.delete_message, name='delete_message'),

    # Admin Modules
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/users/', views.admin_users, name='admin_users'),
    path('admin-panel/users/toggle/<int:user_id>/', views.admin_toggle_user, name='admin_toggle_user'),
    path('admin-panel/logs/', views.admin_logs, name='admin_logs'),
    path('admin-panel/algorithms/', views.admin_algorithms, name='admin_algorithms'),
    path('admin-panel/quiz/', views.admin_quiz, name='admin_quiz'),
    path('admin-panel/messages/', views.admin_messages, name='admin_messages'),
    path('admin-panel/messages/reply/<int:msg_id>/', views.admin_reply_message, name='admin_reply_message'),
    path('admin-panel/announcements/', views.admin_announcements, name='admin_announcements'),
    path('admin-panel/announcements/toggle/<int:ann_id>/', views.admin_toggle_announcement, name='admin_toggle_announcement'),
    path('admin-panel/keys/', views.admin_keys, name='admin_keys'),
    path('admin-panel/activity/', views.admin_activity, name='admin_activity'),
    path('admin-panel/reports/', views.admin_reports, name='admin_reports'),
]
