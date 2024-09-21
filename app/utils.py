from passlib.context import CryptContext
import jwt
from datetime import timedelta, datetime
from .constants import ACCESS_TOKEN_EXPIRY


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_password_hash(password: str):
    hashed = password_context.hash(password)
    return hashed

def verify_password_hash(password: str, hash: str):
    return password_context.verify(password, hash)

def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool = False):
    payload = {
        'user': user_data,
        'exp': datetime.utcnow() + (expiry if expiry is not None else timedelta(minutes=ACCESS_TOKEN_EXPIRY)),
        'refresh': refresh
    }
    token = jwt.encode(
        payload=payload,
        key='Notallkeysaresecret@123',  # This should be stored securely in .env file, not hardcoded
        algorithm='HS256'
    )

    return token


def decode_token(token: str):
    try:
        token_data = jwt.decode(
            jwt = token,
            key = 'Notallkeysaresecret@123', # This should be stored securely in .env file, not hardcoded
            algorithms=['HS256']
        )
        # print('indecodetoken', token_data)
        return token_data, ''
    except jwt.PyJWTError as e:
        print('errorindecoding=>', e)
        return None, e
        # HttpException(status_code=400, detail="Email already registered")