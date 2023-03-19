import base64
import hashlib
import hmac

import jwt

from typing import Union

from flask import current_app, request
from flask_restx import abort

from project.config import BaseConfig


# Функция генерации хеш-пароля
def __generate_password_digest(password: str) -> bytes:
    return hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=current_app.config["PWD_HASH_SALT"],
        iterations=current_app.config["PWD_HASH_ITERATIONS"],
    )


# Функция генерации хеш-пароля
def generate_password_hash(password: str) -> str:
    return base64.b64encode(__generate_password_digest(
        password)).decode('utf-8')


# Сравнение вводимого пароля и пароля, хранящегося в БД
def compose_passwords(password_hash: Union[str, bytes], password: str) -> bool:
    return hmac.compare_digest(
        base64.b64decode(password_hash),
        hashlib.pbkdf2_hmac('sha256',
                            password.encode('utf-8'),
                            current_app.config["PWD_HASH_SALT"],
                            current_app.config["PWD_HASH_ITERATIONS"])
    )

def auth_required(func):
    def wrapper(*args, **kwargs):
        if "Authorization" not in request.headers:
            abort(401)

        data = request.headers["Authorization"]
        token = data.split("Bearer ")[-1]

        try:
            jwt.decode(token, BaseConfig.SECRET_KEY, BaseConfig.JWT_ALGORITHM)
        except Exception as e:
            print("JWT Decode Exception", e)
            abort(401)

        return func(*args, **kwargs)

    return wrapper


def get_email_from_token():

    if "Authorization" not in request.headers:
        abort(401)

    data = request.headers["Authorization"]
    token = data.split("Bearer ")[-1]
    email = None

    try:
        user = jwt.decode(token, BaseConfig.SECRET_KEY, BaseConfig.JWT_ALGORITHM)
        email = user.get("email")

    except Exception as e:
        print("Нет email", e)
        abort(401)

    return email



