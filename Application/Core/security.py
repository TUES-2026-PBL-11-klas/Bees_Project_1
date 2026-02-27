from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Хешира дадена парола.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверява дали дадена парола съвпада с хеширания запис.
    """
    return pwd_context.verify(plain_password, hashed_password)