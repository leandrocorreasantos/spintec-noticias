from api import db
from slugify import slugify
from werkzeug.security import generate_password_hash, check_password_hash


class BaseModel:
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


class User(db.Model, BaseModel):
    __tablename__ = 'users'

    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    # User information
    first_name = db.Column(db.String(100), nullable=False, server_default='')
    last_name = db.Column(db.String(100), nullable=False, server_default='')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Autor(db.Model, BaseModel):
    __tablename__ = 'autors'

    nome = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)


class Noticia(db.Model, BaseModel):
    __tablename__ = 'noticias'

    titulo = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), nullable=False, unique=True)
    texto = db.Column(db.Text())
    autor_id = db.Column(
        db.BigInteger(),
        db.ForeignKey(
            'autors.id',
            ondelete='CASCADE',
            onupdate='CASCADE'
        )
    )
    autor = db.relationship('Autor', backref='noticia', lazy=True)

    def __setattr__(self, key, value):
        super(Noticia, self).__setattr__(key, value)
        if key == 'titulo':
            self.slug = slugify(value)
