import xml.etree.cElementTree as ET
import hashlib
from abc import ABC, abstractmethod


class DefaultRequest(ABC):
    def __init__(self):
        self.mid = ""
        self.pid = ""
        self.password_hash = ""
        self.params = {
            'requesttype': "",
            'apiversion': "2.2.0"
        }

    @abstractmethod
    def get_request_endpoint(self):
        pass

    def build(self):
        data = ET.Element(
            "data", self.params)

        ET.SubElement(data, "default_params",
                      mid=self.mid,
                      pid=self.pid,
                      passwordhash=hashlib.md5(self.password_hash.encode('utf-8')).hexdigest()
                      )

        return data


class DefaultResponse(ABC):
    def __init__(self, root: ET):
        self.error_code = int(root.attrib['errorcode'])

    def is_successful(self) -> bool:
        return self.error_code == 0


class ErrorResponse(DefaultResponse):
    def __init__(self, root: ET):
        super().__init__(root)
        self.customer_message = root.attrib['customermessage']
        self.developer_message = root.attrib['developermessage']
        self.merchant_message = root.attrib['merchantmessage']
        self.response_type = root.attrib['responsetype']

    def __str__(self):
        return ('ErrorResponse(\n'
                'customer_message: {customer_message}\n'
                'developer_message: {developer_message}\n'
                'merchant_message: {merchant_message}\n'
                'response_type: {response_type}'
                ')\n').format(**self.__dict__)




