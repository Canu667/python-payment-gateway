from abc import ABC, abstractmethod
from models.payment_model import PaymentModel
from schemas.payment import PaymentDto


class Provider(ABC):
    @abstractmethod
    def create_payment(self, payment: PaymentDto):
        pass

    def capture(self, payment: PaymentModel):
        pass


class CouldNotInitialisePayment(Exception):
    def __init__(self, order_id, message):
        super(CouldNotInitialisePayment, self).__init__(
            "Payment {} could not be initalised: {} ".format(order_id, message))


class CouldNotCaptureOnPayment(Exception):
    def __init__(self, order_id, message):
        super(CouldNotCaptureOnPayment, self).__init__(
            "Payment {} could not be captured: {} ".format(order_id, message))


class CouldNotActivatePayment(Exception):
    def __init__(self, order_id, message):
        super(CouldNotActivatePayment, self).__init__(
            "Payment {} could not be activated: {} ".format(order_id, message))