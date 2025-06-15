from cryptography.fernet import Fernet
import base64
import hashlib
import os

def get_user_key(user_id: int) -> bytes:
    """根据用户ID生成加密密钥"""
    master_key = os.getenv('MASTER_KEY', 'your-default-master-key-32-chars')
    user_salt = f"user_{user_id}_salt"
    key_material = hashlib.pbkdf2_hmac('sha256', master_key.encode(), user_salt.encode(), 100000)
    return base64.urlsafe_b64encode(key_material[:32])

def encrypt_content(content: str, user_id: int) -> str:
    """加密内容"""
    key = get_user_key(user_id)
    f = Fernet(key)
    return f.encrypt(content.encode()).decode()

def decrypt_content(encrypted_content: str, user_id: int) -> str:
    """解密内容"""
    key = get_user_key(user_id)
    f = Fernet(key)
    return f.decrypt(encrypted_content.encode()).decode()