from flask_restful import Resource
from http import HTTPStatus
from schemas.payment import PaymentDto, PaymentResponseDto, ReservedPaymentDto
from models.payment_model import PaymentModel, PaymentStatus
from domain.payment_manager import PaymentManager
from marshmallow import ValidationError
from flask import request
import injector


class PaymentResource(Resource):
    def get(self, payment_id: int):
        
        payment = PaymentModel().get_by_id(payment_id)
        
        if payment is None:
            return {'message': 'Payment not found'}, HTTPStatus.NOT_FOUND

        response_dto = PaymentResponseDto(**{
            'id': payment.id,
            'payment_method': payment.payment_method,
            'amount': payment.amount,
        })

        return response_dto.dump(), HTTPStatus.OK


class PaymentCreateResource(Resource):
    @injector.inject
    def __init__(self, payment_manager: PaymentManager):
        self._payment_manager = payment_manager

    def post(self):
        json_data = request.get_json()

        try:
            payment_dto = PaymentDto(**json_data)
        except ValidationError as e:
            return {'message': 'Validation errors', 'errors': e.normalized_messages()}, HTTPStatus.BAD_REQUEST

        response = self._payment_manager.create_payment(payment_dto)

        payment = PaymentModel()
        payment.payment_method = payment_dto.payment_configuration.payment_method
        payment.reference_id = payment_dto.reference_id
        payment.amount = payment_dto.order.gross_amount
        payment.status = PaymentStatus.RESERVED
        payment.transaction_id = response.transaction_id
        payment.save()

        response_dto = PaymentResponseDto(**{
            'id': payment.id,
            'payment_method': payment.payment_method,
            'amount': payment.amount
        })
        return response_dto.dump(), HTTPStatus.CREATED


class PaymentCaptureResource(Resource):
    @injector.inject
    def __init__(self, payment_manager: PaymentManager):
        self._payment_manager = payment_manager

    def post(self):
        payment = initialise_payment()

        self._payment_manager.capture(payment)

        payment.status = PaymentStatus.CAPTURED
        payment.save()

        return None, HTTPStatus.OK


class PaymentActivateResource(Resource):
    @injector.inject
    def __init__(self, payment_manager: PaymentManager):
        self._payment_manager = payment_manager

    def post(self):
        payment = initialise_payment()

        self._payment_manager.create_invoice(payment)

        payment.status = PaymentStatus.FINISHED
        payment.save()

        return None, HTTPStatus.OK


def initialise_payment():
    json_data = request.get_json()

    try:
        payment_capture_dto = ReservedPaymentDto(**json_data)
    except ValidationError as e:
        return {'message': 'Validation errors', 'errors': e.normalized_messages()}, HTTPStatus.BAD_REQUEST

    return PaymentModel().get_by_id(payment_capture_dto.id)
