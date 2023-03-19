
from flask import request, abort
from flask_restx import Namespace, Resource

from project.container import user_service
from project.setup.api.models import user
from project.tools.security import auth_required, get_email_from_token

api = Namespace('users')


@api.route('/') # информация о пользователе в БД
class UserView(Resource):

    @api.response(200, description='OK')
    @api.marshal_with(user)
    def get(self):
        """
        Получаем информацию о пользователе!
        """
        token = request.headers['Authorization'].split('Bearer ')[-1]

        if token is None:
            abort(400, "Информация пользователя отсутствует")

        user_data = user_service.get_by_token(token)

        return user_data, 200



    @auth_required
    def patch(self):
        """
        Изменяем информацию пользователя (имя или фамилия или любимый жанр).
        """

        token = request.headers['Authorization'].split('Bearer ')[-1]
        data_user = request.json
        data_user["email"] = get_email_from_token()


        if token is None:
            abort(400, "Не правильный токен")

        return user_service.update(data_user), 201


@api.route('/password/') # Обновление пароля пользователя
class UserView(Resource):
    def put(self):
        """
        Обновляем пароль пользователя.
        """
        data = request.json
        email = data.get('email', None)
        password_one = data.get('password_one', None)
        password_two = data.get('password_two', None)

        if None in [email, password_one, password_two]:
            abort(400, "Не достаточно данных для обновления пароля!")


        user_service.update_password(email, password_one, password_two)

        return "OK", 202
