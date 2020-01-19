from schemas.payment import PaymentDto
from models.payment_model import PaymentModel
from domain.providers.BillpayProvider import BillpayProvider
from domain.providers.billpay.BillpayClient import BillpayClient
from injector import Module, Binder, singleton, inject
from flask import Flask


class PaymentManager:
    @inject
    def __init__(self, billpay_provider: BillpayProvider):
        self._providers = {
            'billpay': billpay_provider
        }

    def create_payment(self, payment: PaymentDto):
        if payment.payment_configuration.payment_method not in self._providers:
            raise PaymentMethodNotImplementedError(payment.payment_configuration.payment_method)

        print("Got " + payment.payment_configuration.payment_method)

        return self._providers[payment.payment_configuration.payment_method].create_payment(payment)

    def capture(self, payment: PaymentModel):
        return self._providers[payment.payment_method].capture(payment)

    def create_invoice(self, payment: PaymentModel):
        return self._providers[payment.payment_method].create_invoice(payment)


class PaymentMethodNotImplementedError(Exception):
    def __init__(self, payment_method: str):
        super(PaymentMethodNotImplementedError, self).__init__(
            "Payment method {} not implemented".format(payment_method))


class PaymentManagerModule(Module):
    def __init__(self, app: Flask):
        self._app = app

    def configure(self, binder: Binder) -> None:
        billpay_private_client = BillpayClient(
            self._app.config.get('BILLPAY_MERCHANT_ID'),
            self._app.config.get('BILLPAY_PRIVATE_PORTAL_ID'),
            self._app.config.get('BILLPAY_PRIVATE_PASSWORD_HASH'),
            self._app.config.get('BILLPAY_API_URL')
        )

        billpay_business_client = BillpayClient(
            self._app.config.get('BILLPAY_MERCHANT_ID'),
            self._app.config.get('BILLPAY_BUSINESS_PORTAL_ID'),
            self._app.config.get('BILLPAY_BUSINESS_PASSWORD_HASH'),
            self._app.config.get('BILLPAY_API_URL')
        )

        billpay_provider = BillpayProvider(billpay_private_client, billpay_business_client)

        binder.bind(
            BillpayProvider,
            to=billpay_provider,
            scope=singleton
        )
