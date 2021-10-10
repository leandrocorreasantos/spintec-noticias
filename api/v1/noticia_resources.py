from sqlalchemy import and_
from http.client import OK
from flask import jsonify, request
from flask.views import MethodView
from api import log, db
from api.v1.schema import (
    NoticiaSchema,
    InternalServerErrorSchema,
    ValidationErrorSchema,
    NotFoundSchema,
    EmptyDataSchema
)
from marshmallow import ValidationError
from api.models import Autor, Noticia
from flask_jwt_extended import jwt_required


class NoticiaView(MethodView):
    def get(self, noticia_slug=None):
        filters = []
        noticias = []
        noticia = []
        autor = None
        pagination = {}
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        titulo = request.args.get('titulo', None, type=str)
        texto = request.args.get('texto', None, type=str)
        autor_name = request.args.get('autor', None, type=str)

        # get one
        if noticia_slug:
            noticia = Noticia.query.filter(
                Noticia.slug == noticia_slug
            ).first()
            if noticia is None:
                log.info("Noticia not found")
                return NotFoundSchema().build()

            return NoticiaSchema().build_response(noticia)

        # filtros
        if titulo:
            filters.append(Noticia.titulo.ilike(r"%{}%".format(titulo)))
        if texto:
            filters.append(Noticia.texto.ilike(r"%{}%".format(texto)))
        if autor_name:
            autor = Autor.query.filter(
                Autor.nome.ilike(r"%{}%".format(autor_name))
            ).first()
            filters.append(Noticia.autor_id == autor.id)

        noticias = Noticia.query.filter(
            and_(*filters)
        ).paginate(page, per_page, False)

        total_pages = int(noticias.total / noticias.per_page)

        pagination = {
            'page': noticias.page,
            'per_page': noticias.per_page,
            'total': noticias.total,
            'total_pages': total_pages,
            'data': NoticiaSchema(many=True).dump(noticias.items)
        }

        return jsonify(pagination), OK.value

    @jwt_required()
    def post(self):
        data = request.get_json()
        if not data:
            return EmptyDataSchema().build()

        try:
            new_noticia = NoticiaSchema().load(data)
        except ValidationError as err:
            return ValidationErrorSchema().build(err.messages)

        noticia = Noticia(**new_noticia)

        try:
            db.session.add(noticia)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            log.error("Error during add noticia: {}".format(e))
            return InternalServerErrorSchema().build()

        return NoticiaSchema().created(noticia)

    @jwt_required()
    def put(self, noticia_slug=None):
        data = request.get_json()
        if not data:
            return EmptyDataSchema().build()

        noticia = Noticia.query.filter(
            Noticia.slug == noticia_slug
        ).first()

        if not noticia:
            log.error('Noticia not found')
            return NotFoundSchema().build()

        try:
            new_noticia = NoticiaSchema().load(data)
        except ValidationError as err:
            log.error("Error while validate noticia: {}".format(err))
            return ValidationErrorSchema().build(err.message)

        noticia.update(**new_noticia)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            log.error("Error during update post: {}".format(e))
            return InternalServerErrorSchema().build()

        return NoticiaSchema().build_response(noticia)

    @jwt_required()
    def delete(self, noticia_slug):
        noticia = Noticia.query.filter(
            Noticia.slug == noticia_slug
        ).first()

        if not noticia:
            log.info('noticia not found')
            return NotFoundSchema().build()

        try:
            db.session.delete(noticia)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            log.error("Error during delete noticia: {}".format(e))
            return InternalServerErrorSchema().build()

        return jsonify({}), OK.value
