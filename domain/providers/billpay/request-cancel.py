from CancelRequest import CancelRequest, CancelResponse
import xml.etree.cElementTree as ET
import requests
import os

obj = CancelRequest("0000008", 1475, "EUR")

obj.mid = os.environ['BILLPAY_MERCHANT_ID']
obj.pid = os.environ['BILLPAY_PORTAL_ID']
obj.password_hash = os.environ['BILLPAY_PASSWORD_HASH']

xmlstr = ET.tostring(obj.build(), encoding='utf8', method='xml').decode()
print("\nXML Sent: {}".format(xmlstr))

headers = {'Content-Type': 'application/xml/'}
r = requests.post('https://test-api.billpay.de/v2/xml/offline/cancel', data=xmlstr, headers=headers)
print("\nResponse Received: {}".format(r.text))

if r.status_code == 200:
    response = CancelResponse(r.text)
    print("\nThe response:\n{}".format(response))