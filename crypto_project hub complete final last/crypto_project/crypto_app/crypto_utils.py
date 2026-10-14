"""
Cryptography utility functions for all algorithms.
Pure Python implementations - no external crypto libraries needed for classical ciphers.
For AES/RSA: uses Python's built-in hashlib + base64 + secrets.
"""

import base64
import hashlib
import secrets
import string
import json
import struct
import math
from typing import Tuple
from PIL import Image
import io
from django.utils import timezone

# ============================================================
# BLOCKCHAIN LOGIC (Advanced Module)
# ============================================================
def calculate_block_hash(index, timestamp, data, previous_hash, nonce):
    block_string = f"{index}{timestamp}{data}{previous_hash}{nonce}"
    return hashlib.sha256(block_string.encode()).hexdigest()


def mine_new_block(index, data, previous_hash, difficulty=2):
    nonce = 0
    ts = timezone.now().isoformat()
    prefix = '0' * difficulty
    while True:
        hash_val = calculate_block_hash(index, ts, data, previous_hash, nonce)
        if hash_val.startswith(prefix):
            return nonce, hash_val, ts
        nonce += 1


# ============================================================
# STEGANOGRAPHY LOGIC (Advanced Module)
# ============================================================
def encode_image_data(image_file, text):
    """Hide text in image using LSB and return BytesIO object."""
    img = Image.open(image_file)
    if img.mode != 'RGB':
        img = img.convert('RGB')

    encoded = img.copy()
    width, height = img.size

    # Convert text to binary and add a delimiter (using a rare sequence)
    # We use a unique marker for end of text
    binary_text = ''.join(format(ord(i), '08b') for i in text) + '1111111111111110'

    data_idx = 0
    text_len = len(binary_text)

    for y in range(height):
        for x in range(width):
            if data_idx < text_len:
                pixel = list(img.getpixel((x, y)))
                for i in range(3): # R, G, B
                    if data_idx < text_len:
                        pixel[i] = pixel[i] & ~1 | int(binary_text[data_idx])
                        data_idx += 1
                encoded.putpixel((x, y), tuple(pixel))
            else:
                break
        if data_idx >= text_len:
            break

    output = io.BytesIO()
    encoded.save(output, format="PNG")
    output.seek(0)
    return output


def decode_image_data(image_file):
    """Extract text from image hidden via LSB."""
    img = Image.open(image_file)
    binary_text = ""
    width, height = img.size

    # To speed up, we don't need to read the whole image if we find the delimiter
    found_delimiter = False
    for y in range(height):
        for x in range(width):
            pixel = img.getpixel((x, y))
            for i in range(3):
                binary_text += str(pixel[i] & 1)

            if len(binary_text) >= 16 and binary_text[-16:] == '1111111111111110':
                found_delimiter = True
                break
        if found_delimiter:
            break

    # Split into 8-bit chunks
    decoded_text = ""
    for i in range(0, len(binary_text) - 16, 8):
        byte = binary_text[i:i+8]
        decoded_text += chr(int(byte, 2))

    return decoded_text


# ============================================================
# CAESAR CIPHER
# ============================================================
def caesar_encrypt(text: str, shift: int) -> str:
    result = []
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result.append(chr((ord(char) - base + shift) % 26 + base))
        else:
            result.append(char)
    return ''.join(result)


def caesar_decrypt(text: str, shift: int) -> str:
    return caesar_encrypt(text, -shift)


# ============================================================
# VIGENERE CIPHER
# ============================================================
def vigenere_encrypt(text: str, key: str) -> str:
    key = key.upper()
    result = []
    key_idx = 0
    for char in text:
        if char.isalpha():
            if not key: key = "A"
            shift = ord(key[key_idx % len(key)]) - ord('A')
            base = ord('A') if char.isupper() else ord('a')
            result.append(chr((ord(char) - base + shift) % 26 + base))
            key_idx += 1
        else:
            result.append(char)
    return ''.join(result)


def vigenere_decrypt(text: str, key: str) -> str:
    key = key.upper()
    result = []
    key_idx = 0
    for char in text:
        if char.isalpha():
            if not key: key = "A"
            shift = ord(key[key_idx % len(key)]) - ord('A')
            base = ord('A') if char.isupper() else ord('a')
            result.append(chr((ord(char) - base - shift) % 26 + base))
            key_idx += 1
        else:
            result.append(char)
    return ''.join(result)


# ============================================================
# BASE64
# ============================================================
def base64_encode(text: str) -> str:
    return base64.b64encode(text.encode('utf-8')).decode('utf-8')


def base64_decode(text: str) -> str:
    try:
        return base64.b64decode(text.encode('utf-8')).decode('utf-8')
    except Exception:
        return "Invalid Base64 input"


# ============================================================
# HASHING
# ============================================================
def md5_hash(text: str) -> str:
    return hashlib.md5(text.encode('utf-8')).hexdigest()


def sha256_hash(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def sha512_hash(text: str) -> str:
    return hashlib.sha512(text.encode('utf-8')).hexdigest()


# ============================================================
# XOR CIPHER (simple symmetric)
# ============================================================
def xor_encrypt(text: str, key: str) -> str:
    if not key:
        return text
    result = []
    for i, char in enumerate(text):
        result.append(chr(ord(char) ^ ord(key[i % len(key)])))
    encrypted = ''.join(result)
    return base64.b64encode(encrypted.encode('latin-1')).decode('utf-8')


def xor_decrypt(text: str, key: str) -> str:
    try:
        decoded = base64.b64decode(text.encode('utf-8')).decode('latin-1')
        result = []
        for i, char in enumerate(decoded):
            result.append(chr(ord(char) ^ ord(key[i % len(key)])))
        return ''.join(result)
    except Exception:
        return "Invalid input for XOR decryption"


# ============================================================
# ROT13
# ============================================================
def rot13(text: str) -> str:
    return text.translate(str.maketrans(
        'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
        'NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm'
    ))


# ============================================================
# ATBASH CIPHER
# ============================================================
def atbash(text: str) -> str:
    result = []
    for char in text:
        if char.isalpha():
            if char.isupper():
                result.append(chr(ord('Z') - (ord(char) - ord('A'))))
            else:
                result.append(chr(ord('z') - (ord(char) - ord('a'))))
        else:
            result.append(char)
    return ''.join(result)


# ============================================================
# AES-LIKE (simplified XOR-based block cipher for demo)
# Real AES requires cryptography library
# ============================================================
def simple_aes_encrypt(text: str, key: str) -> str:
    """Simplified AES-like encryption using key-derived XOR + Base64."""
    key_hash = hashlib.sha256(key.encode()).digest()
    padded = text.encode('utf-8')
    result = bytes([padded[i] ^ key_hash[i % 32] for i in range(len(padded))])
    return base64.b64encode(result).decode('utf-8')


def simple_aes_decrypt(text: str, key: str) -> str:
    """Simplified AES-like decryption."""
    try:
        key_hash = hashlib.sha256(key.encode()).digest()
        decoded = base64.b64decode(text.encode('utf-8'))
        result = bytes([decoded[i] ^ key_hash[i % 32] for i in range(len(decoded))])
        return result.decode('utf-8')
    except Exception:
        return "Decryption failed: Invalid key or ciphertext"


# ============================================================
# RSA-LIKE (simplified for small numbers - demo purposes)
# ============================================================
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def mod_inverse(e, phi):
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x
    _, x, _ = extended_gcd(e, phi)
    return (x % phi + phi) % phi


def generate_rsa_keys_demo():
    """Generate small RSA keys for demonstration."""
    p, q = 61, 53  # Small primes for demo
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 17
    d = mod_inverse(e, phi)
    return {
        'public_key': f"({e}, {n})",
        'private_key': f"({d}, {n})",
        'n': n, 'e': e, 'd': d
    }


def rsa_demo_encrypt(text: str) -> Tuple[str, dict]:
    """Demo RSA encryption (only works for short text with small keys)."""
    keys = generate_rsa_keys_demo()
    e, n = keys['e'], keys['n']
    try:
        encrypted = [pow(ord(c), e, n) for c in text[:20]]  # limit to 20 chars
        return json.dumps(encrypted), keys
    except Exception as ex:
        return str(ex), keys


def rsa_demo_decrypt(ciphertext: str, d: int, n: int) -> str:
    """Demo RSA decryption."""
    try:
        encrypted = json.loads(ciphertext)
        decrypted = ''.join([chr(pow(c, d, n)) for c in encrypted])
        return decrypted
    except Exception:
        return "Decryption failed"


# ============================================================
# KEY GENERATOR
# ============================================================
def generate_random_key(length: int = 32, key_type: str = 'hex') -> str:
    if key_type == 'hex':
        return secrets.token_hex(length // 2)
    elif key_type == 'alphanumeric':
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(length))
    elif key_type == 'base64':
        return base64.b64encode(secrets.token_bytes(length)).decode('utf-8')
    else:
        return secrets.token_urlsafe(length)


# ============================================================
# MASTER ENCRYPT/DECRYPT DISPATCHER
# ============================================================
def perform_encryption(algorithm: str, text: str, key: str = '', operation: str = 'ENCRYPT') -> dict:
    result = {'success': False, 'output': '', 'error': '', 'key_used': key}
    
    try:
        if algorithm == 'CAESAR':
            shift = int(key) if key.isdigit() else 3
            result['key_used'] = str(shift)
            if operation == 'ENCRYPT':
                result['output'] = caesar_encrypt(text, shift)
            else:
                result['output'] = caesar_decrypt(text, shift)

        elif algorithm == 'VIGENERE':
            k = key if key else 'SECRET'
            result['key_used'] = k
            if operation == 'ENCRYPT':
                result['output'] = vigenere_encrypt(text, k)
            else:
                result['output'] = vigenere_decrypt(text, k)

        elif algorithm == 'BASE64':
            if operation == 'ENCRYPT':
                result['output'] = base64_encode(text)
            else:
                result['output'] = base64_decode(text)

        elif algorithm == 'MD5':
            result['output'] = md5_hash(text)

        elif algorithm == 'SHA256':
            result['output'] = sha256_hash(text)

        elif algorithm == 'SHA512':
            result['output'] = sha512_hash(text)

        elif algorithm == 'XOR':
            k = key if key else generate_random_key(8, 'alphanumeric')
            result['key_used'] = k
            if operation == 'ENCRYPT':
                result['output'] = xor_encrypt(text, k)
            else:
                result['output'] = xor_decrypt(text, k)

        elif algorithm == 'ROT13':
            result['output'] = rot13(text)

        elif algorithm == 'ATBASH':
            result['output'] = atbash(text)

        elif algorithm == 'AES':
            k = key if key else generate_random_key(32, 'hex')
            result['key_used'] = k
            if operation == 'ENCRYPT':
                result['output'] = simple_aes_encrypt(text, k)
            else:
                result['output'] = simple_aes_decrypt(text, k)

        elif algorithm == 'RSA':
            if operation == 'ENCRYPT':
                cipher, keys = rsa_demo_encrypt(text)
                result['output'] = cipher
                result['key_used'] = json.dumps(keys)
            else:
                try:
                    k = json.loads(key)
                    result['output'] = rsa_demo_decrypt(text, k['d'], k['n'])
                except Exception:
                    result['output'] = rsa_demo_decrypt(text, 2753, 3233)

        result['success'] = True

    except Exception as e:
        result['error'] = str(e)

    return result
