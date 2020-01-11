from abc import ABC, abstractmethod
from models.payment import Payment


class Provider(ABC):
    @abstractmethod
    def create_payment(self, payment: Payment) -> Payment:
        pass


class CouldNotInitialisePayment(Exception):
    def __init__(self, order_id, message):
        super(CouldNotInitialisePayment, self).__init__(
            "Payment {} could not be initalised: {} ".format(order_id, message))
