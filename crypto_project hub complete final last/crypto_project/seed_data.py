"""
Management command to seed the database with initial data.
Run: python manage.py seed_data
"""

import os
import sys
import django

# ── Allow running directly: python seed_data.py ──────────────────────────────
if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crypto_project.settings')
    django.setup()
# ─────────────────────────────────────────────────────────────────────────────

from django.contrib.auth.models import User
from crypto_app.models import (
    AlgorithmReference, QuizQuestion, Announcement, UserProfile
)


def seed_algorithms():
    algorithms = [
        {
            'name': 'Caesar Cipher',
            'acronym': 'CAESAR',
            'category': 'CLASSICAL',
            'description': 'One of the simplest and most widely known encryption techniques. It is a substitution cipher in which each letter in the plaintext is replaced by a letter some fixed number of positions down the alphabet.',
            'history': 'Named after Julius Caesar, who used it in his private correspondence. The cipher is historically significant as one of the earliest known uses of encryption for practical communication.',
            'how_it_works': 'Each letter is shifted by a fixed number (the "key" or shift). For example, with a shift of 3: A→D, B→E, C→F, etc. To decrypt, the process is reversed by shifting back by the same amount.',
            'use_cases': 'Educational purposes, simple obfuscation, puzzle games, and historical study. Not suitable for any real-world security application.',
            'strengths': 'Extremely simple to understand and implement. Good for educational purposes and demonstrating the concept of substitution ciphers.',
            'weaknesses': 'Trivially broken by brute force (only 25 possible shifts). Vulnerable to frequency analysis. Provides no real security.',
            'key_length': '1 integer (1–25)',
            'complexity': 'LOW',
            'is_featured': True,
        },
        {
            'name': 'Vigenere Cipher',
            'acronym': 'VIGENERE',
            'category': 'CLASSICAL',
            'description': 'A polyalphabetic substitution cipher that uses a keyword to vary the Caesar shift for each letter, making it significantly stronger than a simple Caesar cipher.',
            'history': 'Described by Giovan Battista Bellaso in 1553 and later misattributed to Blaise de Vigenère. It was considered unbreakable for three centuries and was known as "le chiffre indéchiffrable".',
            'how_it_works': 'The keyword is repeated to match the length of the plaintext. Each letter of the plaintext is shifted by the value of the corresponding keyword letter (A=0, B=1, ..., Z=25). This creates a polyalphabetic substitution.',
            'use_cases': 'Historical military communication, educational demonstrations of polyalphabetic ciphers, and cipher challenges.',
            'strengths': 'Much stronger than Caesar cipher. Resistant to simple frequency analysis due to multiple shift values.',
            'weaknesses': 'Vulnerable to Kasiski examination and index of coincidence analysis. Key length can be discovered statistically.',
            'key_length': 'Any word or phrase',
            'complexity': 'LOW',
            'is_featured': True,
        },
        {
            'name': 'Advanced Encryption Standard',
            'acronym': 'AES',
            'category': 'SYMMETRIC',
            'description': 'The gold standard of symmetric encryption. AES is a block cipher that operates on 128-bit blocks of data using keys of 128, 192, or 256 bits. It is the most widely deployed symmetric encryption algorithm in the world.',
            'history': 'Established by NIST in 2001 after a 5-year public competition. It replaced DES and 3DES. Based on the Rijndael algorithm designed by Belgian cryptographers Joan Daemen and Vincent Rijmen.',
            'how_it_works': 'AES processes data in 4×4 byte matrices. It performs multiple rounds (10, 12, or 14 depending on key size) of four transformations: SubBytes (S-box substitution), ShiftRows, MixColumns, and AddRoundKey.',
            'use_cases': 'HTTPS/TLS, file encryption, VPNs, Wi-Fi security (WPA2/WPA3), disk encryption (BitLocker, FileVault), messaging apps, government communications.',
            'strengths': 'Extremely secure against all known attacks. Very fast in hardware. Standardized and widely reviewed. Available in all major programming languages and platforms.',
            'weaknesses': 'Key management is critical — a weak or leaked key completely compromises security. In ECB mode, identical plaintext blocks produce identical ciphertext (use CBC or GCM modes).',
            'key_length': '128, 192, or 256 bits',
            'complexity': 'HIGH',
            'is_featured': True,
        },
        {
            'name': 'RSA Encryption',
            'acronym': 'RSA',
            'category': 'ASYMMETRIC',
            'description': 'RSA (Rivest–Shamir–Adleman) is the most widely used asymmetric encryption algorithm. It uses a mathematically linked public/private key pair — anything encrypted with the public key can only be decrypted with the private key.',
            'history': 'Published in 1977 by Ron Rivest, Adi Shamir, and Leonard Adleman at MIT. The underlying mathematics (modular exponentiation with large primes) had been discovered earlier by Clifford Cocks at GCHQ but was classified.',
            'how_it_works': 'Based on the practical difficulty of factoring the product of two large prime numbers. The public key (e, n) and private key (d, n) are derived from two large primes p and q. Encryption: c = m^e mod n. Decryption: m = c^d mod n.',
            'use_cases': 'HTTPS certificate authentication, digital signatures, SSH key authentication, email encryption (PGP), secure key exchange for symmetric encryption.',
            'strengths': 'No shared secret needed. Enables digital signatures. Foundation of internet security infrastructure. Well-studied for over 45 years.',
            'weaknesses': 'Much slower than symmetric encryption. Vulnerable to quantum computers (Shor\'s algorithm). Key sizes must be 2048+ bits for current security.',
            'key_length': '2048–4096 bits (minimum 2048 recommended)',
            'complexity': 'HIGH',
            'is_featured': True,
        },
        {
            'name': 'SHA-256 Hash',
            'acronym': 'SHA256',
            'category': 'HASH',
            'description': 'SHA-256 (Secure Hash Algorithm 256-bit) is a cryptographic hash function from the SHA-2 family. It produces a fixed 256-bit (32-byte) digest from input of any length, and is computationally infeasible to reverse.',
            'history': 'Published in 2001 by the NSA as part of the SHA-2 standard. Became the dominant hash algorithm after SHA-1 was found vulnerable. Widely adopted for Bitcoin, TLS certificates, and software integrity verification.',
            'how_it_works': 'Processes input in 512-bit blocks through 64 rounds of a compression function using bitwise operations, modular addition, and message schedule. Output is always exactly 256 bits regardless of input size.',
            'use_cases': 'Bitcoin and cryptocurrency, TLS/SSL certificate fingerprints, password hashing (with salt), file integrity verification, digital signatures, HMAC authentication.',
            'strengths': 'Collision resistant (no two inputs produce the same hash). One-way (cannot reverse to find input). Deterministic. Small change in input produces completely different hash (avalanche effect).',
            'weaknesses': 'Not suitable for password storage without salting and key stretching (use bcrypt/Argon2 for passwords). SHA-256 alone is fast — attackers can hash billions of guesses per second.',
            'key_length': 'No key (keyless hash function)',
            'complexity': 'MEDIUM',
            'is_featured': True,
        },
        {
            'name': 'SHA-512 Hash',
            'acronym': 'SHA512',
            'category': 'HASH',
            'description': 'SHA-512 is a member of the SHA-2 family producing a 512-bit (64-byte) digest. It offers higher security margin than SHA-256 and is often faster than SHA-256 on 64-bit processors.',
            'history': 'Published alongside SHA-256 in FIPS 180-2 (2001). Designed to provide a higher security level for applications requiring larger hash outputs.',
            'how_it_works': 'Similar to SHA-256 but operates on 1024-bit blocks with 80 rounds, 64-bit word sizes, and different constants. Produces a 512-bit digest.',
            'use_cases': 'High-security applications, archival integrity, password hashing schemes, digital signatures requiring maximum security.',
            'strengths': 'Higher security margin than SHA-256. Faster than SHA-256 on modern 64-bit CPUs. Provides 256-bit security level.',
            'weaknesses': 'Larger output size may be unnecessary for many applications. Like all SHA-2 variants, not suitable for password hashing without key stretching.',
            'key_length': 'No key (keyless hash function)',
            'complexity': 'MEDIUM',
            'is_featured': False,
        },
        {
            'name': 'MD5 Hash',
            'acronym': 'MD5',
            'category': 'HASH',
            'description': 'MD5 (Message-Digest Algorithm 5) is a widely used hash function producing a 128-bit digest. While once a cryptographic standard, MD5 is now considered cryptographically broken and unsuitable for security purposes.',
            'history': 'Designed by Ronald Rivest in 1991 as an improvement to MD4. Widely adopted through the 1990s and 2000s. In 2004, researchers demonstrated practical collision attacks, effectively ending its use in security.',
            'how_it_works': 'Processes data in 512-bit blocks through 4 rounds of 16 operations each, using modular addition, bitwise operations, and a per-round constant table. Produces a 128-bit output.',
            'use_cases': 'File integrity checksums (non-security), database deduplication, legacy systems, non-security checksums. NOT for passwords or security.',
            'strengths': 'Fast computation. Widely supported. Useful for non-security checksums and deduplication.',
            'weaknesses': 'Cryptographically broken — collisions can be generated in seconds. Do NOT use for passwords, certificates, or any security purpose.',
            'key_length': 'No key (keyless hash function)',
            'complexity': 'LOW',
            'is_featured': False,
        },
        {
            'name': 'Base64 Encoding',
            'acronym': 'BASE64',
            'category': 'ENCODING',
            'description': 'Base64 is an encoding scheme (NOT encryption) that converts binary data into an ASCII string format using 64 printable characters. It is used to safely transmit binary data over text-based protocols.',
            'history': 'Developed in the early days of email (MIME standard) to allow binary attachments to be sent over SMTP, which was designed for 7-bit ASCII text only.',
            'how_it_works': 'Takes 3 bytes (24 bits) of binary data at a time and converts them into 4 ASCII characters from the Base64 alphabet (A-Z, a-z, 0-9, +, /). Padding characters (=) are added if needed.',
            'use_cases': 'Email attachments (MIME), embedding images in HTML/CSS as data URIs, storing binary data in JSON, HTTP Basic Authentication headers, JWT tokens.',
            'strengths': 'Universal support. Allows binary data in text-only contexts. Reversible without any key.',
            'weaknesses': 'NOT encryption — anyone can decode Base64 trivially. Increases data size by ~33%. Provides zero security on its own.',
            'key_length': 'No key (not encryption)',
            'complexity': 'LOW',
            'is_featured': False,
        },
        {
            'name': 'ROT-13 Cipher',
            'acronym': 'ROT13',
            'category': 'CLASSICAL',
            'description': 'ROT13 is a simple letter substitution cipher that replaces each letter with the letter 13 positions after it in the alphabet. It is a special case of the Caesar cipher with a fixed shift of 13.',
            'history': 'Used in online forums in the early internet era (especially Usenet) to hide spoilers, offensive content, or puzzle solutions. The name means "rotate by 13 places".',
            'how_it_works': 'Since the alphabet has 26 letters, applying ROT13 twice returns to the original text. A→N, B→O, ..., M→Z, N→A, etc. The same function is used for both encoding and decoding.',
            'use_cases': 'Hiding spoilers in forum posts, obfuscating puzzle solutions, simple examples in programming education.',
            'strengths': 'Self-inverse — applying ROT13 twice gives the original. Easy to implement.',
            'weaknesses': 'Trivially broken. Only one possible "key". Provides absolutely no security.',
            'key_length': 'No key (fixed shift of 13)',
            'complexity': 'LOW',
            'is_featured': False,
        },
        {
            'name': 'Atbash Cipher',
            'acronym': 'ATBASH',
            'category': 'CLASSICAL',
            'description': 'Atbash is a classical Hebrew substitution cipher that reverses the alphabet. A maps to Z, B maps to Y, C maps to X, and so on. It is also self-inverse.',
            'history': 'Originally used to encode Hebrew names in the Bible (e.g., Babel = Sheshach in Jeremiah). The name comes from the first, last, second, and second-to-last letters of the Hebrew alphabet.',
            'how_it_works': 'Each letter is replaced by its mirror opposite in the alphabet. Position 1 (A) ↔ Position 26 (Z), Position 2 (B) ↔ Position 25 (Y), etc. No key is needed.',
            'use_cases': 'Historical study, educational demonstrations, puzzle games, and cipher challenges.',
            'strengths': 'Self-inverse. Simple to understand and explain.',
            'weaknesses': 'No key — completely deterministic. Trivially reversible. Zero security.',
            'key_length': 'No key',
            'complexity': 'LOW',
            'is_featured': False,
        },
        {
            'name': 'XOR Cipher',
            'acronym': 'XOR',
            'category': 'SYMMETRIC',
            'description': 'The XOR cipher applies the exclusive-or (XOR) operation between each byte of the plaintext and the corresponding byte of a repeating key. It is the fundamental building block of many modern ciphers.',
            'history': 'XOR as a cipher has been used since the early days of computing. It forms the core operation in stream ciphers and is used internally in AES (AddRoundKey step), AES-CTR, ChaCha20, and many other modern algorithms.',
            'how_it_works': 'Each bit of plaintext is XOR\'d with the corresponding bit of the key. If key and plaintext bit are the same → 0; different → 1. Applying XOR with the same key again restores the original plaintext.',
            'use_cases': 'Building block in stream ciphers, AES AddRoundKey step, simple obfuscation, CTR and OFB block cipher modes.',
            'strengths': 'Extremely fast. Perfectly secure when used with a truly random key of the same length as the message (One-Time Pad). Simple to implement.',
            'weaknesses': 'Vulnerable to known-plaintext attacks when key is reused. Short repeating keys are easily broken by frequency analysis.',
            'key_length': 'Any length (longer is stronger)',
            'complexity': 'LOW',
            'is_featured': True,
        },
    ]

    count = 0
    for algo_data in algorithms:
        _, created = AlgorithmReference.objects.get_or_create(
            acronym=algo_data['acronym'],
            defaults=algo_data
        )
        if created:
            count += 1
            print(f"  ✅ Added: {algo_data['name']}")
        else:
            print(f"  ⏭  Exists: {algo_data['name']}")
    print(f"  → {count} new algorithms added.")


def seed_quiz_questions():
    questions = [
        {
            'question': 'Which encryption algorithm is considered the current global standard for symmetric encryption?',
            'option_a': 'DES (Data Encryption Standard)',
            'option_b': 'AES (Advanced Encryption Standard)',
            'option_c': 'RSA (Rivest-Shamir-Adleman)',
            'option_d': 'MD5',
            'correct_answer': 'B',
            'explanation': 'AES was established by NIST in 2001 and is the most widely deployed symmetric cipher. DES is obsolete, RSA is asymmetric, and MD5 is a hash function.',
            'difficulty': 'EASY',
        },
        {
            'question': 'What is the fundamental difference between symmetric and asymmetric encryption?',
            'option_a': 'Symmetric is faster; asymmetric is slower',
            'option_b': 'Symmetric uses the same key for encryption and decryption; asymmetric uses different keys',
            'option_c': 'Symmetric uses two keys; asymmetric uses one key',
            'option_d': 'Symmetric is more secure than asymmetric',
            'correct_answer': 'B',
            'explanation': 'Symmetric encryption uses the same key for both operations. Asymmetric encryption uses a public key for encryption and a private key for decryption (or vice versa for signatures).',
            'difficulty': 'EASY',
        },
        {
            'question': 'What does a cryptographic hash function guarantee?',
            'option_a': 'The output can be reversed to find the original input',
            'option_b': 'The same input always produces the same output, and the output cannot be reversed',
            'option_c': 'The output size always equals the input size',
            'option_d': 'Only the key holder can compute the hash',
            'correct_answer': 'B',
            'explanation': 'Hash functions are deterministic (same input → same output) and one-way (cannot reverse the output to find the input). This is called pre-image resistance.',
            'difficulty': 'EASY',
        },
        {
            'question': 'The Caesar cipher with a shift of 13 is known as:',
            'option_a': 'Vigenere cipher',
            'option_b': 'Atbash cipher',
            'option_c': 'ROT13',
            'option_d': 'XOR cipher',
            'correct_answer': 'C',
            'explanation': 'ROT13 (Rotate 13) is a special case of the Caesar cipher with a fixed shift of 13. Because 13+13=26 (the alphabet length), applying ROT13 twice returns the original text.',
            'difficulty': 'EASY',
        },
        {
            'question': 'RSA encryption security is based on the computational difficulty of:',
            'option_a': 'Solving differential equations',
            'option_b': 'Computing discrete logarithms',
            'option_c': 'Factoring the product of two large prime numbers',
            'option_d': 'Reversing SHA-256 hash functions',
            'correct_answer': 'C',
            'explanation': 'RSA security relies on the fact that while multiplying two large primes is easy, factoring the result back into those primes is computationally infeasible with current technology.',
            'difficulty': 'MEDIUM',
        },
        {
            'question': 'Which of the following is NOT a property of a secure cryptographic hash function?',
            'option_a': 'Pre-image resistance',
            'option_b': 'Collision resistance',
            'option_c': 'Reversibility',
            'option_d': 'Avalanche effect',
            'correct_answer': 'C',
            'explanation': 'Secure hash functions must be irreversible (one-way). Pre-image resistance, collision resistance, and the avalanche effect (small change in input → completely different output) are all desirable security properties.',
            'difficulty': 'MEDIUM',
        },
        {
            'question': 'What is the key weakness of the Vigenere cipher that makes it breakable?',
            'option_a': 'It uses too short a key',
            'option_b': 'The keyword repeats, allowing frequency analysis after finding key length via Kasiski examination',
            'option_c': 'It only works on uppercase letters',
            'option_d': 'It uses the same shift for every letter',
            'correct_answer': 'B',
            'explanation': 'The Vigenere cipher repeats the keyword. The Kasiski examination finds repeated ciphertext segments to determine key length, then frequency analysis breaks each Caesar shift independently.',
            'difficulty': 'MEDIUM',
        },
        {
            'question': 'Base64 is best described as:',
            'option_a': 'A strong symmetric encryption algorithm',
            'option_b': 'An encoding scheme to represent binary data as ASCII text — not encryption',
            'option_c': 'A hash function producing 64-character output',
            'option_d': 'A key derivation function',
            'correct_answer': 'B',
            'explanation': 'Base64 is purely an encoding scheme, not encryption. It is trivially reversible without any key. It converts binary data to printable ASCII characters for use in text-based protocols like email and HTTP.',
            'difficulty': 'EASY',
        },
        {
            'question': 'What is the "avalanche effect" in cryptography?',
            'option_a': 'The rapid increase in key size needed as computers get faster',
            'option_b': 'A small change in input causing a completely different output',
            'option_c': 'The cascading failure of encryption when one key is compromised',
            'option_d': 'Using multiple encryption layers for stronger security',
            'correct_answer': 'B',
            'explanation': 'The avalanche effect means that even a single bit change in the input (or key) results in about 50% of the output bits changing. This is a critical property of strong cryptographic functions.',
            'difficulty': 'MEDIUM',
        },
        {
            'question': 'Why is MD5 no longer recommended for security-sensitive applications?',
            'option_a': 'It is too slow for modern hardware',
            'option_b': 'Practical collision attacks have been demonstrated — two different inputs can produce the same MD5 hash',
            'option_c': 'Its output is too long at 512 bits',
            'option_d': 'It requires a secret key to operate',
            'correct_answer': 'B',
            'explanation': 'MD5 was broken in 2004 when researchers demonstrated that collisions (two different inputs with the same hash) could be generated rapidly. This makes MD5 unsuitable for digital signatures, certificates, or any security purpose.',
            'difficulty': 'MEDIUM',
        },
    ]

    count = 0
    for q_data in questions:
        _, created = QuizQuestion.objects.get_or_create(
            question=q_data['question'],
            defaults=q_data
        )
        if created:
            count += 1
    print(f"  → {count} new quiz questions added.")


def seed_announcements(admin_user):
    announcements_data = [
        {
            'title': '🎉 Welcome to CryptoHub!',
            'content': 'Welcome to CryptoHub — your complete platform for learning cryptography! Explore 11 encryption algorithms, take quizzes, manage cryptographic keys, and track your progress. Start with the Encryption Tool to try your first cipher!',
            'priority': 'HIGH',
            'target_audience': 'ALL',
            'is_active': True,
        },
        {
            'title': '📚 New Algorithm Documentation Added',
            'content': 'We have added detailed documentation for all 11 supported algorithms including AES, RSA, Caesar, Vigenere, Atbash, ROT13, XOR, Base64, MD5, SHA-256, and SHA-512. Visit the Algorithm Reference section to learn about each one.',
            'priority': 'MEDIUM',
            'target_audience': 'ALL',
            'is_active': True,
        },
        {
            'title': '🧠 Quiz Module Now Available',
            'content': 'Test your cryptography knowledge with our new quiz module! 10 questions covering encryption theory, algorithm properties, and security concepts. Take a quiz from your dashboard and track your scores over time.',
            'priority': 'MEDIUM',
            'target_audience': 'USERS',
            'is_active': True,
        },
    ]

    count = 0
    for ann_data in announcements_data:
        _, created = Announcement.objects.get_or_create(
            title=ann_data['title'],
            defaults={**ann_data, 'created_by': admin_user}
        )
        if created:
            count += 1
    print(f"  → {count} new announcements added.")


def seed_admin():
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@cryptohub.edu',
            password='admin123',
            first_name='Admin',
            last_name='CryptoHub'
        )
        UserProfile.objects.create(
            user=admin,
            expertise_level='EXPERT',
            organization='CryptoHub',
            bio='Platform administrator'
        )
        print("  ✅ Admin user created: username=admin, password=admin123")
        return admin
    else:
        print("  ⏭  Admin user already exists.")
        return User.objects.get(username='admin')


def seed_demo_user():
    if not User.objects.filter(username='demo').exists():
        user = User.objects.create_user(
            username='demo',
            email='demo@cryptohub.edu',
            password='demo1234',
            first_name='Demo',
            last_name='User'
        )
        UserProfile.objects.create(
            user=user,
            expertise_level='INTERMEDIATE',
            organization='CryptoHub Demo',
            bio='Demo account for testing the platform.'
        )
        print("  ✅ Demo user created: username=demo, password=demo1234")
    else:
        print("  ⏭  Demo user already exists.")


def run():
    print("\n🔐 CryptoHub Database Seeder")
    print("=" * 45)

    print("\n[1/5] Creating admin user...")
    admin_user = seed_admin()

    print("\n[2/5] Creating demo user...")
    seed_demo_user()

    print("\n[3/5] Seeding algorithm documentation...")
    seed_algorithms()

    print("\n[4/5] Seeding quiz questions...")
    seed_quiz_questions()

    print("\n[5/5] Seeding announcements...")
    seed_announcements(admin_user)

    print("\n" + "=" * 45)
    print("✅ Database seeded successfully!\n")
    print("🚀 Run the server:")
    print("   python manage.py runserver")
    print("\n🔑 Login credentials:")
    print("   Admin  → username: admin    | password: admin123")
    print("   User   → username: demo     | password: demo1234")
    print("\n🌐 URLs:")
    print("   Homepage  → http://127.0.0.1:8000/")
    print("   Login     → http://127.0.0.1:8000/login/")
    print("   Dashboard → http://127.0.0.1:8000/dashboard/")
    print("   Admin     → http://127.0.0.1:8000/admin-panel/")
    print("=" * 45 + "\n")


if __name__ == '__main__':
    run()
