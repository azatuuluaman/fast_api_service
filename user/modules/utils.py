import os
import random
import string
from typing import Union, Any
from datetime import datetime, timedelta

import redis
import smtplib
from jose import jwt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from passlib.context import CryptContext

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.environ.get(
    "JWT_SECRET_KEY", "your-secret-key"
)  # should be kept secret
JWT_REFRESH_SECRET_KEY = os.environ.get(
    "JWT_REFRESH_SECRET_KEY", "your-refresh-secret-key"
)  # should be kept secret

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=REFRESH_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def get_redis() -> redis.Redis:
    return redis.Redis(host="redis", port=6379, decode_responses=True)


def send_code(email: str, code: str):
    s = smtplib.SMTP(host="smtp.gmail.com", port=587)
    s.starttls()
    s.login(os.environ.get("EMAIL_ADDRESS"), os.environ.get("EMAIL_PASSWORD"))
    msg = MIMEMultipart()
    msg["From"] = os.environ.get("MY_ADDRESS")
    msg["To"] = email
    msg["Subject"] = "Email Activation"
    msg.attach(MIMEText(f"activate with {code}", "plain"))
    s.send_message(msg)
    s.quit()


def get_code_by_email(email: str) -> str:
    with get_redis() as r:
        code = r.get(email)

    if code is None:
        raise ValueError("incorrect email")

    return code


def get_random_string(length: int):
    letters = string.ascii_lowercase
    result_str = "".join(random.choice(letters) for _ in range(length))
    return result_str
