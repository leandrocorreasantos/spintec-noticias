from marshmallow import Schema, fields, validate
from flask import jsonify
from http.client import (
    NOT_FOUND,
    OK,
    CREATED,
    BAD_REQUEST,
    INTERNAL_SERVER_ERROR
)


class BaseSchema(Schema):
    pagination = fields.Dict()

    def build_response(self, data, pagination=None):
        if pagination:
            return jsonify(
                {'items': self.dump(data), 'pagination': pagination}
            ), OK.value
        return jsonify(self.dump(data)), OK.value

    @classmethod
    def build(cls, data):
        return jsonify(cls().dump(data)), OK.value

    def created(self, data):
        return jsonify(self.dump(data)), CREATED.value


class UserSchema(BaseSchema):
    id = fields.Integer()
    username = fields.String(validate=validate.Length(max=100, min=3))
    password = fields.String(
        validate=validate.Length(min=6, max=255)
    )
    email = fields.String()
    first_name = fields.String()
    last_name = fields.String()


class AutorSchema(BaseSchema):
    id = fields.Integer()
    nome = fields.String(validate=validate.Length(min=3, max=200))
    email = fields.Email()


class NoticiaSchema(BaseSchema):
    id = fields.Integer()
    titulo = fields.String(validate=validate.Length(min=3, max=200))
    slug = fields.String()
    texto = fields.String()
    autor = fields.Nested('AutorSchema')
    autor_id = fields.Integer(load_only=True)


# ERROR MESSAGES


class InternalServerErrorSchema(Schema):
    message = fields.String(default="Internal Server Error")
    code = fields.Integer(default=INTERNAL_SERVER_ERROR)
    description = fields.String(default="Internal Server Error")

    @classmethod
    def build(cls, message=None):
        return jsonify(cls().dump(
            {"message": message}
        )), INTERNAL_SERVER_ERROR.value


class EmptyDataSchema(Schema):
    message = fields.String(default="Empty data")
    code = fields.Integer(default=BAD_REQUEST)
    description = fields.String(default="Request data is empty")

    @classmethod
    def build(cls):
        return jsonify(cls().dump({})), BAD_REQUEST.value


# NOT FOUND
class NotFoundSchema(Schema):
    message = fields.String(default="Not Found")
    code = fields.Integer(default=NOT_FOUND)
    description = fields.String(default="Data Not Found")

    @classmethod
    def build(cls):
        return jsonify(cls().dump({})), NOT_FOUND.value


# VALIDATION ERROR


class ValidationErrorSchema(Schema):
    description = fields.Dict()

    def build(self, description):
        return jsonify(self.dump(
            {'description': description}
        )), BAD_REQUEST.value
