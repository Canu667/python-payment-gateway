import xml.etree.cElementTree as ET
import hashlib


class DefaultRequest:
    def __init__(self):
        self._request_type = ""
        self.api_version = "2.2.0"
        self.mid = ""
        self.pid = ""
        self.password_hash = ""
        self.params = {
            'requesttype': self._request_type,
            'apiversion': self.api_version
        }

    def build(self):
        data = ET.Element(
            "data", self.params)

        ET.SubElement(data, "default_params",
                      mid=self.mid,
                      pid=self.pid,
                      passwordhash=hashlib.md5(self.password_hash.encode('utf-8')).hexdigest()
                      )

        return data
