import sys
import errno
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from api import app, db, log
from api.models import User
from werkzeug.security import generate_password_hash


migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def seed():
    user = {
        "id": 1,
        "username": "admin",
        "password": generate_password_hash("12345678"),
        "email": "admin@localhost",
        "first_name": "admin",
        "last_name": "admin",
    }

    try:
        db.session.add(User(**user))
        db.session.commit()
    except Exception as e:
        log.error("Erro ao adicionar usuario: {}".format(e))
        db.session.rollback()


if __name__ == '__main__':
    if not app.debug:
        log.error('App is in production mode. Migration skipped')
        sys.exit(errno.EACCES)
    manager.run()
