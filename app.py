from flask import Flask
from flask_restful import Api
from resources.payment import (
    PaymentResource,
    PaymentCreateResource,
    PaymentCaptureResource,
    PaymentActivateResource
)
from extensions import db
from flask_migrate import Migrate
from flask_injector import FlaskInjector
from injector import Injector
from domain.payment_manager import PaymentManagerModule


def register_extensions(app):
    db.init_app(app)
    Migrate(app, db)

    injector = Injector([PaymentManagerModule(app)])
    FlaskInjector(app=app, injector=injector)


def register_resources(app):
    api = Api(app)

    api.add_resource(PaymentResource, '/payment/<int:payment_id>')
    api.add_resource(PaymentCreateResource, '/payment')
    api.add_resource(PaymentCaptureResource, '/payment/capture')
    api.add_resource(PaymentActivateResource, '/payment/activate')


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
