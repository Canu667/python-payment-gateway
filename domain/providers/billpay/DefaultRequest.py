import xml.etree.cElementTree as ET
import hashlib

class DefaultRequest():
    def __init__(self):
        self._requesttype = ""
        self.apiversion = "2.2.0"
        self.mid = ""
        self.pid = ""
        self.passwordhash = ""
        self.params = {
            'requesttype' : self._requesttype,
            'apiversion' : self.apiversion
        }

    def build(self):
        data = ET.Element(
            "data", self.params)

        ET.SubElement(data, "default_params",
                      mid=self.mid,
                      pid=self.pid,
                      passwordhash=hashlib.md5(self.passwordhash.encode('utf-8')).hexdigest()
                      )

        return data
