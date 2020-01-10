from CaptureRequest import CaptureRequest, CaptureResponse
import xml.etree.cElementTree as ET
import requests
import os
from pprint import pprint

obj = CaptureRequest('18cceb8d-6db4-43fa-979e-1b7c65dd0f26', 1475, "EUR", "0000008")

obj.mid = os.environ['BILLPAY_MERCHANT_ID']
obj.pid = os.environ['BILLPAY_PORTAL_ID']
obj.password_hash = os.environ['BILLPAY_PASSWORD_HASH']

xmlstr = ET.tostring(obj.build(), encoding='utf8', method='xml').decode()
print("\nXML Sent: {}".format(xmlstr))

headers = {'Content-Type': 'application/xml/'}
r = requests.post('https://test-api.billpay.de/v2/xml/offline/capture', data=xmlstr, headers=headers)
print("\nResponse Received: {}".format(r.text))

if r.status_code == 200:
    response = CaptureResponse(r.text)
    print("\nThe response:\n{}".format(response))