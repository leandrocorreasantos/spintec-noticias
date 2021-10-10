import os
import sys
import logging
import logging.config
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

dotenv_path = os.path.join(os.getcwd(), '.env')
if os.path.isfile(dotenv_path):
    from dotenv import load_dotenv
    load_dotenv(dotenv_path)

app.config.from_object(os.environ.get('CONFIG_OBJECT'))

db = SQLAlchemy(app)
jwt = JWTManager(app)

CORS(app, resources={r"/v1/*": {"origins": "*"}})

handler = logging.StreamHandler(sys.stdout)

if not app.debug:
    handler = logging.handlers.SysLogHandler(address='/dev/log')

formater = logging.Formatter(
    '{"timestamp": "%(asctime)s",'
    '"level": "%(levelname)s",'
    '"message": "%(message)s",'
    '"file": "%(filename)s",'
    '"line": "%(lineno)s"}'
)
handler.setFormatter(formater)

log = logging.getLogger(os.environ.get('LOGGER_NAME', __name__))
log.setLevel(int(os.environ.get('LOG_LEVEL', logging.INFO)))
log.addHandler(handler)
