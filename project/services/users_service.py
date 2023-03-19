import jwt

from project.dao import UserDAO
from project.setup.api.models import user
from project.tools.security import generate_password_hash, compose_passwords
from project.config import BaseConfig


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, uid):
        """
        Сервис получения одного пользователя

        """
        return self.dao.get_one(uid)

    def get_all(self):
        """
        Сервис получения всех пользователей

        """
        return self.dao.get_all()

    def get_by_email(self, email):
        """
        Сервис поиска пользователя по логину (email)

        """
        return self.dao.get_by_email(email)

    def get_by_token(self, token):
        """
        Сервис поиска пользователя по токену (email)

        """
        user_data = jwt.decode(token, BaseConfig.SECRET_KEY, algorithms=[BaseConfig.JWT_ALGORITHM])
        return self.get_by_email(user_data['email'])


    def create(self, user_data: dict[str, str]):
        """
        Сервис создания пользователя

        """
        user_data['password'] = generate_password_hash(user_data.get('password'))
        return self.dao.create(user_data)

    def update(self, user_data):
        """
        Сервис обновления данных о пользователе

        """
        user = self.get_by_email(user_data.get("email"))
        if "name" in user_data:
            user.name = user_data.get("name")
        if "surname" in user_data:
            user.surname = user_data.get("surname")
        if "favourite_genre_id" in user_data:
            user.favourite_genre_id = user_data.get("favourite_genre_id")

        self.dao.update(user)
        return "", 204

    def update_password(self, email, current_password, new_password):
        """
        Сервис обновления пароля пользователя

        """

        user = self.get_by_email(email)

        if compose_passwords(user.password, current_password):

            self.dao.update_password(email, new_password)


    def delete(self, uid):
        """
        Сервис удаления пользователя

        """
        self.dao.delete(uid)


