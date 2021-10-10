import os
from api import app as application
from api.v1.user_resources import UserView as v1_User
from api.v1.user_resources import LoginView as v1_Login
from api.v1.autor_resources import AutorView as v1_Autor
from api.v1.noticia_resources import NoticiaView as v1_Noticia

# module autor
application.add_url_rule(
    '/v1/autor',
    view_func=v1_Autor.as_view('autores'),
    methods=['GET', 'POST']
)

application.add_url_rule(
    '/v1/autor/<int:autor_id>',
    view_func=v1_Autor.as_view('autor'),
    methods=['GET', 'PUT', 'DELETE']
)

# module noticia
application.add_url_rule(
    '/v1/noticia',
    view_func=v1_Noticia.as_view('noticias'),
    methods=['GET', 'POST']
)

application.add_url_rule(
    '/v1/noticia/<noticia_slug>',
    view_func=v1_Noticia.as_view('noticia'),
    methods=['GET', 'PUT', 'DELETE']
)

# module user
application.add_url_rule(
    '/v1/user',
    view_func=v1_User.as_view('users'),
    methods=['GET', 'POST']
)

application.add_url_rule(
    '/v1/user/<user_id>',
    view_func=v1_User.as_view('user'),
    methods=['PUT', 'DELETE']
)

application.add_url_rule(
    '/v1/user/login',
    view_func=v1_Login.as_view('login'),
    methods=['POST']
)


if __name__ == '__main__':
    application.run(debug=application.debug,
                    host=os.environ.get('HOST', '0.0.0.0'),
                    port=int(os.environ.get('PORT', 5000)))
