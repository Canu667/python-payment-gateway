from InvoiceCreatedRequest import create_response, InvoiceCreatedRequest
import xml.etree.cElementTree as ET
import requests
import os

obj = InvoiceCreatedRequest(1475, "EUR", "0000008", 1)

obj.mid = os.environ['BILLPAY_MERCHANT_ID']
obj.pid = os.environ['BILLPAY_PORTAL_ID']
obj.password_hash = os.environ['BILLPAY_PASSWORD_HASH']

obj.invoice_amount_net = 1250
obj.invoice_amount_gross = 1475
obj.shipping_name = "Express-Versand"
obj.shipping_price_net = 500
obj.shipping_price_gross = 650

xmlstr = ET.tostring(obj.build(), encoding='utf8', method='xml').decode()
print("\nXML Sent: {}".format(xmlstr))

headers = {'Content-Type': 'application/xml/'}
r = requests.post('https://test-api.billpay.de/v2/xml/offline/invoiceCreated', data=xmlstr, headers=headers)
print("\nResponse Received: {}".format(r.text))

if r.status_code == 200:
    response = create_response(r.text)
    print("\nThe response:\n{}".format(response))
