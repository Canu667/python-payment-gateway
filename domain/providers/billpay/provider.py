# from GetBillPayBankData import GetBillPayBankData
from domain.providers.provider import Provider
from models.payment import Payment
import xml.etree.cElementTree as ET
# import requests


class BillpayProvider(Provider):
    def create_payment(self, payment: Payment) -> None:
        request = PreauthorizeRequest()
