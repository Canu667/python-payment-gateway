from PreauthorizeRequest import PreauthorizeRequest, PreauthorizeResponse
from CaptureRequest import CaptureRequest, CaptureResponse
from InvoiceCreatedRequest import InvoiceCreatedRequest, InvoiceCreatedResponse
from CancelRequest import CancelRequest, CancelResponse
from DefaultRequest import DefaultRequest, ErrorResponse
import xml.etree.cElementTree as ET
import requests


class BillpayClient:
    def __init__(self, mid: str, pid: str, password_hash: str):
        self._mid = mid
        self._pid = pid
        self._password_hash = password_hash
        self.url = 'https://test-api.billpay.de/v2/xml/offline'

    def preauthorise(self, obj: PreauthorizeRequest) -> PreauthorizeResponse:
        return self._send_request(obj)

    def capture(self, obj: CaptureRequest) -> CaptureResponse:
        return self._send_request(obj)

    def create_invoice(self, obj: InvoiceCreatedRequest) -> InvoiceCreatedResponse:
        return self._send_request(obj)

    def cancel(self, obj: CancelRequest) -> CancelResponse:
        return self._send_request(obj)

    def _send_request(self, obj: DefaultRequest):
        obj.mid = self._mid
        obj.pid = self._pid
        obj.password_hash = self._password_hash

        xmlstr = ET.tostring(obj.build(), encoding='utf8', method='xml').decode()
        print(xmlstr)

        headers = {'Content-Type': 'application/xml/'}
        r = requests.post(self.url + obj.get_request_endpoint(), data=xmlstr, headers=headers)

        print(r.text)
        if r.status_code == 200:
            return self.create_response(r.text)
        else:
            raise RuntimeError('Failed to send request to Billpay')

    def create_response(self, xml: str):
        root = ET.fromstring(xml)
        error_code = int(root.attrib['errorcode'])
        response_type = root.attrib['responsetype']

        if error_code == 0:
            return {
                PreauthorizeRequest.TYPE: PreauthorizeResponse,
                CancelRequest.TYPE: CancelResponse,
                CaptureRequest.TYPE: CaptureResponse,
                InvoiceCreatedRequest.TYPE: InvoiceCreatedResponse,
            }[response_type](root)
        else:
            return ErrorResponse(root)
