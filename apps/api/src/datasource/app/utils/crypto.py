from cryptography.fernet import Fernet
from app.core.config import settings
import base64


def _get_key():
    """获取加密密钥"""
    # 使用配置中的secret_key生成固定的加密密钥
    key = base64.urlsafe_b64encode(settings.secret_key.encode()[:32].ljust(32, b'0'))
    return key


def encrypt_password(password: str) -> str:
    """加密密码"""
    if not password:
        return password
    
    key = _get_key()
    f = Fernet(key)
    encrypted = f.encrypt(password.encode())
    return base64.urlsafe_b64encode(encrypted).decode()


def decrypt_password(encrypted_password: str) -> str:
    """解密密码"""
    if not encrypted_password:
        return encrypted_password
    
    try:
        key = _get_key()
        f = Fernet(key)
        encrypted_bytes = base64.urlsafe_b64decode(encrypted_password.encode())
        decrypted = f.decrypt(encrypted_bytes)
        return decrypted.decode()
    except Exception:
        # 如果解密失败，可能是未加密的密码，直接返回
        return encrypted_password
