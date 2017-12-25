import logging.config

from flask import Flask, Blueprint

from blog_app.api import api
from blog_app.api.routes.auth.auth import ns as auth_ns
from blog_app.api.routes.blog.articles import ns as articles_ns
from blog_app.api.routes.blog.categories import ns as categories_ns
from blog_app.config import settings
from blog_app.database import db

logging.config.fileConfig('config/logging.conf')
log = logging.getLogger(__name__)

app = Flask(__name__)


def configure():
    app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME

    app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS

    app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP


def initialize():
    configure()

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(auth_ns)
    api.add_namespace(articles_ns)
    api.add_namespace(categories_ns)
    app.register_blueprint(blueprint)

    db.init_app(app)


initialize()

if __name__ == '__main__':
    log.info('>>> Starting development server at http://{}/api/ <<<'.format(app.config['SERVER_NAME']))
    app.run(debug=settings.FLASK_DEBUG)
