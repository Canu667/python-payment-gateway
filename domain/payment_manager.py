from models.payment import Payment
from domain.providers.billpay.provider import BillpayProvider

class PaymentManager:
    def __init__(self):
        self._providers = {
            'billpay': BillpayProvider()
        }

    def create_payment(self, payment: Payment) -> None:
        if payment.payment_method not in self._providers:
            raise PaymentMethodNotImplementedError(payment.payment_method)

        print("Got " + payment.payment_method)

        self._providers[payment.payment_method].create_payment(payment)

class PaymentMethodNotImplementedError(Exception):
    def __init__(self, payment_method):
        super(PaymentMethodNotImplementedError, self).__init__("Payment method {} not implemented".format(payment_method))