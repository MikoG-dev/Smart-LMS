from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hashed(password):
    return pwd_context.hash(password)

def pwdVerify(plain, hashed):
    return pwd_context.verify(plain, hashed)
