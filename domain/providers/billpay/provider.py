# from GetBillPayBankData import GetBillPayBankData
from domain.providers.provider import Provider
from models.payment import Payment
import xml.etree.cElementTree as ET
# import requests


class BillpayProvider(Provider):
    def create_payment(self, payment: Payment) -> None:
        request = PreauthorizeRequest()
        request
        print("Created Billpay Payment")

        # req_data = GetBillPayBankData('13938945')
        # xmlstr = ET.tostring(
        #     req_data.build(), encoding='utf8', method='xml').decode()
        # print(xmlstr)

        # headers = {'Content-Type': 'application/xml/'}
        # r = requests.post(
        #     'https://api.billpay.de/v2/xml/getBillPayBankData', data=xmlstr, headers=headers)
        # print(r.text)
