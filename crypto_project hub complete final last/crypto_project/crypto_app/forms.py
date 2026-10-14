from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile, ContactMessage, CryptoKey, CommunicationMessage


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'autofocus': True
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )


class CustomRegisterForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'})
    )
    expertise_level = forms.ChoiceField(
        choices=[
            ('BEGINNER', 'Beginner'),
            ('INTERMEDIATE', 'Intermediate'),
            ('ADVANCED', 'Advanced'),
            ('EXPERT', 'Expert'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class EncryptionForm(forms.Form):
    ALGORITHM_CHOICES = [
        ('', '-- Select Algorithm --'),
        ('Classical Ciphers', [
            ('CAESAR', 'Caesar Cipher'),
            ('VIGENERE', 'Vigenere Cipher'),
            ('ROT13', 'ROT-13'),
            ('ATBASH', 'Atbash Cipher'),
        ]),
        ('Modern Encryption', [
            ('AES', 'AES (Demo)'),
            ('XOR', 'XOR Cipher'),
            ('RSA', 'RSA (Demo)'),
        ]),
        ('Encoding', [
            ('BASE64', 'Base64'),
        ]),
        ('Hashing', [
            ('MD5', 'MD5'),
            ('SHA256', 'SHA-256'),
            ('SHA512', 'SHA-512'),
        ]),
    ]
    OPERATION_CHOICES = [
        ('ENCRYPT', 'Encrypt / Hash'),
        ('DECRYPT', 'Decrypt / Decode'),
    ]

    algorithm = forms.ChoiceField(
        choices=ALGORITHM_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'algorithm-select'})
    )
    operation = forms.ChoiceField(
        choices=OPERATION_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )
    input_text = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Enter text to encrypt or decrypt...'
        })
    )
    key = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Encryption key (required for some algorithms)'
        })
    )
    save_to_history = forms.BooleanField(required=False, initial=True)


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your@email.com'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Your message...'}),
        }


class KeyGeneratorForm(forms.Form):
    LENGTH_CHOICES = [(16, '16 chars'), (32, '32 chars'), (64, '64 chars'), (128, '128 chars')]
    TYPE_CHOICES = [('hex', 'Hexadecimal'), ('alphanumeric', 'Alphanumeric'), ('base64', 'Base64'), ('urlsafe', 'URL-Safe')]

    key_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Key name/label'})
    )
    algorithm = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. AES-256'})
    )
    length = forms.ChoiceField(choices=LENGTH_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    key_type = forms.ChoiceField(choices=TYPE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
    )


class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = UserProfile
        fields = ['bio', 'phone', 'organization', 'expertise_level', 'preferred_algorithm']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'organization': forms.TextInput(attrs={'class': 'form-control'}),
            'expertise_level': forms.Select(attrs={'class': 'form-control'}),
            'preferred_algorithm': forms.TextInput(attrs={'class': 'form-control'}),
        }


class SendMessageForm(forms.ModelForm):
    receiver = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    algorithm = forms.ChoiceField(
        choices=EncryptionForm.ALGORITHM_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    message_to_encrypt = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Type message here...'})
    )
    encryption_key = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Key to encrypt/decrypt'})
    )

    class Meta:
        model = CommunicationMessage
        fields = ['receiver', 'subject', 'algorithm', 'encryption_key']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
        }
