from passlib.context import CryptContext as _CryptContext


_pwd_context = _CryptContext(schemes=('bcrypt',))


def hash_password(password: str) -> str:
    return _pwd_context.hash(password)


def verify_password(raw_password, hashed_password):
    return _pwd_context.verify(raw_password, hashed_password)
