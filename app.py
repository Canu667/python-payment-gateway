from flask import Flask, request
from flask_restful import Api
from resources.payment import PaymentResource, PaymentCreateResource
from extensions import db
from flask_migrate import Migrate


def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)

def register_resources(app):
    api = Api(app)

    api.add_resource(PaymentResource, '/payment/<int:payment_id>')
    api.add_resource(PaymentCreateResource, '/payment')


def create_app():
    app = Flask(__name__)
    config_str = 'config.Config'
    app.config.from_object(config_str)

    register_resources(app)
    register_extensions(app)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
