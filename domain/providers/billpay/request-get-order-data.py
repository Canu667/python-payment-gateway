from GetBillPayBankData import GetBillPayBankData
import xml.etree.cElementTree as ET
import requests

req_data = GetBillPayBankData('13938945')
req_data.mid = os.environ['BILLPAY_MERCHANT_ID']
req_data.pid = os.environ['BILLPAY_PORTAL_ID']
req_data.passwordhash = os.environ['BILLPAY_PASSWORD_HASH']

xmlstr = ET.tostring(req_data.build(), encoding='utf8', method='xml').decode()
print(xmlstr)

headers = {'Content-Type': 'application/xml/'}
r = requests.post('https://test-api.billpay.de/v2/xml/offline/getBillPayBankData', data=xmlstr, headers=headers)
print(r.text)
