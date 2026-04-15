from flask import request
from flask_restful import Resource

from app.schemas.schemas import LoginSchema, SignupSchema, UserSchema, load_or_raise
from app.services.auth_service import AuthService


class SignupResource(Resource):
    def __init__(self):
        self.auth_service = AuthService()
        self.signup_schema = SignupSchema()
        self.user_schema = UserSchema()

    def post(self):
        payload = load_or_raise(self.signup_schema, request.get_json())
        user = self.auth_service.signup(payload)
        return self.user_schema.dump(user), 201


class LoginResource(Resource):
    def __init__(self):
        self.auth_service = AuthService()
        self.login_schema = LoginSchema()
        self.user_schema = UserSchema()

    def post(self):
        payload = load_or_raise(self.login_schema, request.get_json())
        user = self.auth_service.login(payload)
        return self.user_schema.dump(user), 200


class CheckSessionResource(Resource):
    def __init__(self):
        self.auth_service = AuthService()
        self.user_schema = UserSchema()

    def get(self):
        user = self.auth_service.check_session()
        return self.user_schema.dump(user), 200


class LogoutResource(Resource):
    def __init__(self):
        self.auth_service = AuthService()

    def delete(self):
        self.auth_service.logout()
        return {}, 204
