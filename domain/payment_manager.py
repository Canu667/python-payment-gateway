from models.payment import Payment
from domain.providers.BillpayProvider import BillpayProvider
from domain.providers.billpay.BillpayClient import BillpayClient
from flask import current_app


class PaymentManager:
    def __init__(self):
        self._providers = {
            'billpay': BillpayProvider(
                BillpayClient(
                    current_app.config.get('BILLPAY_MERCHANT_ID'),
                    current_app.config.get('BILLPAY_PRIVATE_PORTAL_ID'),
                    current_app.config.get('BILLPAY_PRIVATE_PASSWORD_HASH'),
                    current_app.config.get('BILLPAY_API_URL')
                ),
                BillpayClient(
                    current_app.config.get('BILLPAY_MERCHANT_ID'),
                    current_app.config.get('BILLPAY_BUSINESS_PORTAL_ID'),
                    current_app.config.get('BILLPAY_BUSINESS_PASSWORD_HASH'),
                    current_app.config.get('BILLPAY_API_URL')
                ),
            )
        }

    def create_payment(self, payment: Payment) -> None:
        if payment.payment_method not in self._providers:
            raise PaymentMethodNotImplementedError(payment.payment_method)

        print("Got " + payment.payment_method)

        self._providers[payment.payment_method].create_payment(payment)


class PaymentMethodNotImplementedError(Exception):
    def __init__(self, payment_method):
        super(PaymentMethodNotImplementedError, self).__init__(
            "Payment method {} not implemented".format(payment_method))
