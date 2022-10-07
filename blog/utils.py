from datetime import datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=['bcrypt'], deprecated='auto')

SECRET_KEY = 'LONGANDRANDOMICSECRETEKEY'
ALGORITHM = 'HS256'


def bcrypt(password: str):
    return pwd_cxt.hash(password)


def verify(plain_password, hashed_password):
    return pwd_cxt.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
