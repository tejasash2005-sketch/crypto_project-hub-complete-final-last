from django.contrib import admin
from .models import (
    EncryptionLog, CryptoKey, FileEncryptionRecord, UserProfile,
    AlgorithmReference, QuizQuestion, QuizAttempt, ContactMessage,
    Announcement, ActivityLog
)

@admin.register(EncryptionLog)
class EncryptionLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'algorithm', 'operation', 'created_at', 'success']
    list_filter = ['algorithm', 'operation', 'success']
    search_fields = ['user__username']

@admin.register(CryptoKey)
class CryptoKeyAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'key_type', 'algorithm', 'is_active', 'created_at']
    list_filter = ['key_type', 'is_active']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'expertise_level', 'total_encryptions', 'total_decryptions']

@admin.register(AlgorithmReference)
class AlgorithmReferenceAdmin(admin.ModelAdmin):
    list_display = ['name', 'acronym', 'category', 'complexity', 'is_featured']
    list_filter = ['category', 'complexity', 'is_featured']

@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ['question', 'correct_answer', 'difficulty', 'is_active']
    list_filter = ['difficulty', 'is_active']

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'score', 'total_questions', 'percentage', 'attempted_at']

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'status', 'created_at']
    list_filter = ['status']

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'priority', 'is_active', 'target_audience', 'created_at']

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'timestamp', 'ip_address']
    list_filter = ['action']
