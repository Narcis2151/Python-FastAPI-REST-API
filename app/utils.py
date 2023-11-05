from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password) -> str:
    return pwd_context.hash(password)


def verify_password(password, encrypted_password) -> bool:
    return pwd_context.verify(password, encrypted_password)
