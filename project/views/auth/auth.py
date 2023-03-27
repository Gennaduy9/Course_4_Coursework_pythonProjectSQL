from flask import request
from flask_restx import Namespace, Resource

from project.container import auth_service, user_service
from project.setup.api.models import auth, auth_result

api = Namespace('auth')


@api.route('/register/') # регистрация (создания) пользователя в БД
class AuthsView(Resource):
    @api.expect(auth)
    @api.response(200, description='OK')
    def post(self):
        """
        Регистрация пользователя!
        """
        user_service.create(request.json)
        return "OK", 200




@api.route('/login/') # Вход пользователя в систему
class AuthView(Resource):
    @api.expect(auth)
    def post(self):
        """
        Аутентификация пользователя
        """
        data = request.json

        email = data.get('email', None)
        password = data.get('password', None)

        if None in [email, password]:
            return "", 400

        tokens = auth_service.generate_tokens(email, password)

        return tokens, 201

    def put(self): # создание новой пары токенов
        """
        Создание новой пары токенов!
        """
        data = request.json
        token = data.get("refresh_token")

        tokens = auth_service.approve_refresh_token(token)

        return tokens, 201
