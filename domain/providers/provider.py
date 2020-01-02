from abc import ABC, abstractmethod
from models.payment import Payment


class Provider():
    @abstractmethod
    def create_payment(self, payment: Payment) -> Payment:
        pass
