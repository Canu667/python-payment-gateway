from flask_restful import Resource
from http import HTTPStatus
from schemas.payment import PaymentSchema
from models.payment import Payment
from domain.payment_manager import PaymentManager
from marshmallow import ValidationError
from flask import request

payment_schema = PaymentSchema()

class PaymentResource(Resource):
    def get(self, payment_id):
        
        payment = Payment().get_by_id(payment_id)
        
        if payment is None:
            return {'message': 'Payment not found'}, HTTPStatus.NOT_FOUND

        return payment_schema.dump(payment), HTTPStatus.OK

class PaymentCreateResource(Resource):
    def post(self):
        json_data = request.get_json()

        try:
            data = payment_schema.load(data=json_data)
        except ValidationError as e:
            return {'message': 'Validation errors', 'errors': e.normalized_messages()}, HTTPStatus.BAD_REQUEST

        payment = Payment(**data)
        payment.save()

        payment_manager = PaymentManager()
        payment_manager.create_payment(payment)

        return payment_schema.dump(payment), HTTPStatus.CREATED
