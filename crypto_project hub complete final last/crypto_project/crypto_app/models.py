from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# ============================================================
# MODULE 1: Encryption History / Logs
# ============================================================
class EncryptionLog(models.Model):
    ALGORITHM_CHOICES = [
        ('AES', 'AES (Advanced Encryption Standard)'),
        ('DES', 'DES (Data Encryption Standard)'),
        ('RSA', 'RSA (Rivest-Shamir-Adleman)'),
        ('CAESAR', 'Caesar Cipher'),
        ('VIGENERE', 'Vigenere Cipher'),
        ('BASE64', 'Base64 Encoding'),
        ('MD5', 'MD5 Hash'),
        ('SHA256', 'SHA-256 Hash'),
        ('SHA512', 'SHA-512 Hash'),
    ]
    OPERATION_CHOICES = [
        ('ENCRYPT', 'Encrypt'),
        ('DECRYPT', 'Decrypt'),
        ('HASH', 'Hash'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='encryption_logs')
    algorithm = models.CharField(max_length=20, choices=ALGORITHM_CHOICES)
    operation = models.CharField(max_length=10, choices=OPERATION_CHOICES)
    input_text = models.TextField(blank=True)
    output_text = models.TextField(blank=True)
    key_used = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    success = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Encryption Log'
        verbose_name_plural = 'Encryption Logs'

    def __str__(self):
        return f"{self.user.username} - {self.algorithm} - {self.operation} ({self.created_at.strftime('%Y-%m-%d')})"


# ============================================================
# MODULE 2: Saved Keys / Key Management
# ============================================================
class CryptoKey(models.Model):
    KEY_TYPE_CHOICES = [
        ('SYMMETRIC', 'Symmetric Key'),
        ('PUBLIC', 'Public Key'),
        ('PRIVATE', 'Private Key'),
        ('SECRET', 'Secret/Passphrase'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='crypto_keys')
    name = models.CharField(max_length=100)
    key_type = models.CharField(max_length=20, choices=KEY_TYPE_CHOICES)
    algorithm = models.CharField(max_length=50)
    key_value = models.TextField()
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Crypto Key'
        verbose_name_plural = 'Crypto Keys'

    def __str__(self):
        return f"{self.name} ({self.key_type}) - {self.user.username}"

    @property
    def is_expired(self):
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False


# ============================================================
# MODULE 3: File Encryption Records
# ============================================================
class FileEncryptionRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='file_records')
    original_filename = models.CharField(max_length=255)
    encrypted_filename = models.CharField(max_length=255, blank=True)
    algorithm = models.CharField(max_length=50)
    file_size = models.BigIntegerField(default=0)
    operation = models.CharField(max_length=10, choices=[('ENCRYPT', 'Encrypt'), ('DECRYPT', 'Decrypt')])
    status = models.CharField(max_length=20, choices=[
        ('SUCCESS', 'Success'), ('FAILED', 'Failed'), ('PENDING', 'Pending')
    ], default='PENDING')
    created_at = models.DateTimeField(default=timezone.now)
    checksum = models.CharField(max_length=128, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'File Encryption Record'

    def __str__(self):
        return f"{self.original_filename} - {self.operation}"


# ============================================================
# MODULE 4: User Profile / Extended Info
# ============================================================
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    organization = models.CharField(max_length=200, blank=True)
    expertise_level = models.CharField(max_length=20, choices=[
        ('BEGINNER', 'Beginner'),
        ('INTERMEDIATE', 'Intermediate'),
        ('ADVANCED', 'Advanced'),
        ('EXPERT', 'Expert'),
    ], default='BEGINNER')
    preferred_algorithm = models.CharField(max_length=20, blank=True)
    total_encryptions = models.IntegerField(default=0)
    total_decryptions = models.IntegerField(default=0)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    joined_at = models.DateTimeField(default=timezone.now)
    last_activity = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Profile: {self.user.username}"


# ============================================================
# MODULE 5: Algorithm Reference / Learning Module
# ============================================================
class AlgorithmReference(models.Model):
    CATEGORY_CHOICES = [
        ('SYMMETRIC', 'Symmetric Encryption'),
        ('ASYMMETRIC', 'Asymmetric Encryption'),
        ('HASH', 'Hash Functions'),
        ('CLASSICAL', 'Classical Ciphers'),
        ('ENCODING', 'Encoding Schemes'),
    ]
    name = models.CharField(max_length=100)
    acronym = models.CharField(max_length=20)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    history = models.TextField(blank=True)
    how_it_works = models.TextField()
    use_cases = models.TextField()
    strengths = models.TextField(blank=True)
    weaknesses = models.TextField(blank=True)
    key_length = models.CharField(max_length=100, blank=True)
    complexity = models.CharField(max_length=20, choices=[
        ('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High')
    ], default='MEDIUM')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.acronym})"


# ============================================================
# MODULE 6: Quiz / Assessment Module
# ============================================================
class QuizQuestion(models.Model):
    question = models.TextField()
    option_a = models.CharField(max_length=300)
    option_b = models.CharField(max_length=300)
    option_c = models.CharField(max_length=300)
    option_d = models.CharField(max_length=300)
    correct_answer = models.CharField(max_length=1, choices=[
        ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')
    ])
    explanation = models.TextField(blank=True)
    difficulty = models.CharField(max_length=10, choices=[
        ('EASY', 'Easy'), ('MEDIUM', 'Medium'), ('HARD', 'Hard')
    ], default='MEDIUM')
    category = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.question[:80]


class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    percentage = models.FloatField(default=0.0)
    time_taken = models.IntegerField(default=0, help_text="Time in seconds")
    attempted_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-attempted_at']

    def __str__(self):
        return f"{self.user.username} - {self.score}/{self.total_questions}"


# ============================================================
# MODULE 7: Contact / Support Messages
# ============================================================
class ContactMessage(models.Model):
    STATUS_CHOICES = [
        ('NEW', 'New'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
        ('CLOSED', 'Closed'),
    ]
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')
    admin_reply = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"


# ============================================================
# MODULE 8: Announcements / Notices
# ============================================================
class Announcement(models.Model):
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]
    title = models.CharField(max_length=200)
    content = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    is_active = models.BooleanField(default=True)
    target_audience = models.CharField(max_length=20, choices=[
        ('ALL', 'All Users'), ('USERS', 'Regular Users'), ('ADMIN', 'Admins Only')
    ], default='ALL')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


# ============================================================
# MODULE 9: Activity / Audit Trail
# ============================================================
class ActivityLog(models.Model):
    ACTION_CHOICES = [
        ('LOGIN', 'User Login'),
        ('LOGOUT', 'User Logout'),
        ('ENCRYPT', 'Encryption'),
        ('DECRYPT', 'Decryption'),
        ('KEY_CREATE', 'Key Created'),
        ('KEY_DELETE', 'Key Deleted'),
        ('PROFILE_UPDATE', 'Profile Updated'),
        ('QUIZ_ATTEMPT', 'Quiz Attempted'),
        ('FILE_UPLOAD', 'File Uploaded'),
        ('PASSWORD_CHANGE', 'Password Changed'),
        ('BLOCKCHAIN_MINE', 'Blockchain Block Mined'),
        ('STEGO_ENCODE', 'Steganography Encoding'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_logs')
    action = models.CharField(max_length=30, choices=ACTION_CHOICES)
    description = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    extra_data = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username} - {self.action} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"


# ============================================================
# MODULE 10: Communication / Secure Messaging
# ============================================================
class CommunicationMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=200, blank=True)
    encrypted_content = models.TextField()
    encryption_key = models.TextField(help_text="The key to decrypt this message")
    algorithm = models.CharField(max_length=50)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Communication Message'
        verbose_name_plural = 'Communication Messages'

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username} - {self.algorithm}"


# ============================================================
# ADVANCED MODULE 11: Blockchain Module
# ============================================================
class BlockchainBlock(models.Model):
    index = models.IntegerField()
    timestamp = models.DateTimeField(default=timezone.now)
    data = models.TextField()
    previous_hash = models.CharField(max_length=64)
    nonce = models.IntegerField(default=0)
    hash = models.CharField(max_length=64)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['index']
        verbose_name = 'Blockchain Block'

    def __str__(self):
        return f"Block #{self.index} [{self.hash[:10]}]"


# ============================================================
# ADVANCED MODULE 12: Steganography Module
# ============================================================
class SteganographyRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_image = models.ImageField(upload_to='stego/original/')
    stego_image = models.ImageField(upload_to='stego/encoded/', null=True, blank=True)
    hidden_text = models.TextField(blank=True)  # Store encrypted text if needed
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Stego Record by {self.user.username} at {self.created_at}"


# ============================================================
# NEW ADVANCED MODULE 13: Professional Security Suite
# ============================================================
class ProfessionalSecurityRecord(models.Model):
    SUITE_CHOICES = [
        ('AES_GCM', 'AES-256-GCM (Authenticated)'),
        ('RSA_PSS', 'RSA Digital Signature'),
        ('ECC_EDDSA', 'ECC (Ed25519) Signing'),
        ('DH_EXCHANGE', 'Diffie-Hellman Key Exchange'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feature_type = models.CharField(max_length=50, choices=SUITE_CHOICES)
    input_data = models.TextField()
    output_data = models.TextField()
    extra_info = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.feature_type} - {self.user.username}"
