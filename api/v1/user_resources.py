from http.client import (
    OK, UNAUTHORIZED
)
from flask import jsonify, request
from flask.views import MethodView
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)
from api import log, db
from api.v1.schema import (
    InternalServerErrorSchema,
    EmptyDataSchema,
    UserSchema,
    NotFoundSchema,
    ValidationErrorSchema
)
from api.models import User


class LoginView(MethodView):
    def post(self):
        # faz login e gera o token jwt
        data = request.get_json()
        if not data:
            log.error('no data')
            return EmptyDataSchema().build()

        username = data['username']
        password = data['password']
        if not username and not password:
            log.error('no username or password')
            return EmptyDataSchema().build()

        user = User.query.filter(
            User.username == username
        ).first()
        if not user:
            log.error('no username found')
            return NotFoundSchema().build()

        if not user:
            log.error('no username found')
            return NotFoundSchema().build()

        if not check_password_hash(user.password, password):
            log.error('diff password')
            return jsonify(
                {'error': 'User or password are incorrect'}
            ), UNAUTHORIZED.value

        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), OK.value


class UserView(MethodView):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        return jsonify(
            logged_in_as=current_user,
        ), OK.value

    @jwt_required
    def post(self):
        data = request.get_json()

        if not data:
            return EmptyDataSchema().build()

        try:
            new_user = UserSchema().load(data)
        except ValidationError as err:
            log.error(err)
            return ValidationErrorSchema().build(err)

        new_user['password'] = generate_password_hash(new_user['password'])

        user = User(**UserSchema().dump(new_user))

        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            log.error(e)
            db.session.rollback()
            return InternalServerErrorSchema().build("Database Error")

        return UserSchema().created(
            UserSchema(exclude=('password',)).dump(user)
        )

    @jwt_required
    def put(self, user_id):
        user_id = int(user_id)
        new_user = None
        data = request.get_json()

        if not data or user_id is None:
            return EmptyDataSchema().build()
        user = User.query.get(user_id)

        if not user:
            return NotFoundSchema().build()

        try:
            new_user = UserSchema().load(data)
        except ValidationError as err:
            return ValidationErrorSchema().build(err.message)

        user.update(**new_user)

        if 'password' in new_user:
            user.password = generate_password_hash(
                new_user['password']
            )

        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            log.error("Error during update user: {}".format(e))
            return InternalServerErrorSchema().build("Database error")

        return UserSchema().build(
            UserSchema(exclude=('password',)).dump(user)
        )

    @jwt_required
    def delete(self, user_id):
        user_id = int(user_id)

        user = User.query.get(user_id)
        if not user:
            return NotFoundSchema().build()

        try:
            db.session.delete(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            log.error("Database Error: {}".format(e))
            return InternalServerErrorSchema().build()

        return jsonify({}), OK.value
