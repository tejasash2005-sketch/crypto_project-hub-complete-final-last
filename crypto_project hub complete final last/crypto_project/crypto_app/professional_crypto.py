import os
import base64
import json
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import rsa, padding, ed25519, dh
import pyotp

# ============================================================
# 1. AES-256-GCM (Authenticated Encryption)
# ============================================================
def prof_aes_encrypt(plaintext: str, password: str) -> dict:
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = kdf.derive(password.encode())
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), None)

    return {
        'ciphertext': base64.b64encode(ciphertext).decode('utf-8'),
        'nonce': base64.b64encode(nonce).decode('utf-8'),
        'salt': base64.b64encode(salt).decode('utf-8')
    }

def prof_aes_decrypt(data_dict: dict, password: str) -> str:
    try:
        salt = base64.b64decode(data_dict['salt'])
        nonce = base64.b64decode(data_dict['nonce'])
        ciphertext = base64.b64decode(data_dict['ciphertext'])

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = kdf.derive(password.encode())
        aesgcm = AESGCM(key)
        decrypted = aesgcm.decrypt(nonce, ciphertext, None)
        return decrypted.decode('utf-8')
    except Exception as e:
        return f"Decryption failed: {str(e)}"

# ============================================================
# 2. RSA (2048-bit with PSS Signatures)
# ============================================================
def prof_rsa_generate_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    priv_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode('utf-8')

    pub_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('utf-8')

    return priv_pem, pub_pem

def prof_rsa_sign(message: str, private_key_pem: str) -> str:
    priv_key = serialization.load_pem_private_key(private_key_pem.encode(), password=None)
    signature = priv_key.sign(
        message.encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return base64.b64encode(signature).decode('utf-8')

def prof_rsa_verify(message: str, signature_b64: str, public_key_pem: str) -> bool:
    try:
        pub_key = serialization.load_pem_public_key(public_key_pem.encode())
        signature = base64.b64decode(signature_b64)
        pub_key.verify(
            signature,
            message.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception:
        return False

# ============================================================
# 3. ECC (Ed25519 Signing)
# ============================================================
def prof_ecc_generate():
    priv_key = ed25519.Ed25519PrivateKey.generate()
    pub_key = priv_key.public_key()

    priv_bytes = priv_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption()
    )
    pub_bytes = pub_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )
    return base64.b64encode(priv_bytes).decode('utf-8'), base64.b64encode(pub_bytes).decode('utf-8')

def prof_ecc_sign(message: str, priv_b64: str) -> str:
    priv_bytes = base64.b64decode(priv_b64)
    priv_key = ed25519.Ed25519PrivateKey.from_private_bytes(priv_bytes)
    signature = priv_key.sign(message.encode())
    return base64.b64encode(signature).decode('utf-8')

# ============================================================
# 4. Diffie-Hellman Key Exchange
# ============================================================
def prof_dh_parameters():
    parameters = dh.generate_parameters(generator=2, key_size=2048)
    return parameters

def prof_dh_generate_keys(parameters):
    priv_key = parameters.generate_private_key()
    pub_key = priv_key.public_key()
    return priv_key, pub_key

# ============================================================
# 5. TOTP (2FA)
# ============================================================
def prof_totp_generate_secret():
    return pyotp.random_base32()

def prof_totp_get_uri(secret: str, username: str):
    return pyotp.totp.TOTP(secret).now()

def prof_totp_verify(secret: str, code: str) -> bool:
    totp = pyotp.totp.TOTP(secret)
    return totp.verify(code)
