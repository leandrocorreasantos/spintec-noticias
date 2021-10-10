from api import db, log
from http.client import OK
from flask import jsonify, request
from flask.views import MethodView
from api.v1.schema import (
    AutorSchema,
    InternalServerErrorSchema,
    NotFoundSchema,
    ValidationErrorSchema,
    EmptyDataSchema
)
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required
from api.models import Autor


class AutorView(MethodView):
    def get(self, autor_id=None):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        autores = None
        autor = None

        if autor_id:
            autor = Autor.query.get(autor_id)
            return AutorSchema().build_response(autor)

        try:
            autores = Autor.query.paginate(page, per_page, False)
        except Exception as e:
            log.error("Error during search autors: {}".format(e))
            return InternalServerErrorSchema().build()

        total_pages = int(autores.total / autores.per_page)

        pagination = {
            'page': autores.page,
            'per_page': autores.per_page,
            'total': autores.total,
            'total_pages': total_pages,
            'data': AutorSchema(many=True).dump(autores.items)
        }

        return jsonify(pagination), OK.value

    @jwt_required()
    def post(self):
        data = request.get_json()
        if not data:
            return EmptyDataSchema().build()

        try:
            autor = AutorSchema().load(data)
        except ValidationError as err:
            log.error('Error validating autor data: {}'.format(err))
            return ValidationErrorSchema().build(err.messages)

        try:
            db.session.add(Autor(**autor))
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            log.error("Error during add autor: {}".format(e))
            return InternalServerErrorSchema().build()

        return AutorSchema().created(autor)

    @jwt_required()
    def put(self, autor_id):
        autor_id = int(autor_id)
        data = request.get_json()
        if not data or autor_id == 0:
            return EmptyDataSchema().build()

        autor = Autor.query.get(autor_id)
        if not autor:
            log.error("Autor not found")
            return NotFoundSchema().build()

        try:
            new_autor = AutorSchema().load(data)
        except ValidationError as err:
            log.error("Error validating autor: {}".format(err))
            return ValidationErrorSchema().build(err.messages)

        autor.update(**new_autor)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            log.error("Error during update autor: {}".format(e))
            return InternalServerErrorSchema().build()

        return AutorSchema().build_response(autor)

    @jwt_required()
    def delete(self, autor_id):
        autor_id = int(autor_id)

        autor = Autor.query.get(autor_id)
        if not autor:
            return NotFoundSchema().build()

        try:
            db.session.delete(autor)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            log.error("Error during delete autor: {}".format(e))
            return InternalServerErrorSchema().build()

        return jsonify({}), OK.value
