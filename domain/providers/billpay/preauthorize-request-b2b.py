from PreauthorizeRequest import CompanyDetails, PreauthorizeRequest, PreauthorizeResponse, CustomerDetails, Total, Article
import xml.etree.cElementTree as ET
import requests
import os

obj = PreauthorizeRequest()

obj.mid = os.environ['BILLPAY_MERCHANT_ID']
obj.pid = os.environ['BILLPAY_BUSINESS_PORTAL_ID']
obj.password_hash = os.environ['BILLPAY_BUSINESS_PASSWORD_HASH']

customer_details = CustomerDetails()
customer_details.customer_id = 123456
customer_details.customer_type = CustomerDetails.EXISTING_CUSTOMER
customer_details.salutation = "Herr"
customer_details.first_name = "Thomas"
customer_details.last_name = "Testkunde"
customer_details.street = "Teststr."
customer_details.street_no = "11"
customer_details.zip = "10115"
customer_details.city = "Berlin"
customer_details.country = "DEU"
customer_details.email = "anyone@anymail.de"
customer_details.phone = "0302333453"
customer_details.cell_phone = "01775112383"
customer_details.birthday = "19740419"
customer_details.language = "de"
customer_details.ip = "85.214.7.10"
customer_details.customer_group = CustomerDetails.GROUP_BUSINESS
obj.customer_details = customer_details

company_details = CompanyDetails()
company_details.name = "Testfirma"
company_details.legal_form = "Gmbh"
company_details.register_number = "HRB 122 029 B"
company_details.holder_name = "Testinhaber"
company_details.tax_number = "DE268874183"
obj.company_details = company_details

total = Total()
total.shipping_name = "Express-Versand"
total.shipping_price_net = 500
total.shipping_price_gross = 650
total.rebate_net = 0
total.rebate_gross = 0
total.order_amount_net = 1250
total.order_amount_gross = 1475
total.currency = "EUR"
total.reference = "0000003"
obj.total = total

article = Article()
article.article_id = "1234"
article.article_name = "test1"
article.article_type = "0"
article.article_quantity = "1"
article.article_price_net = "250"
article.article_price_gross = "275"
obj.add_article(article)

article2 = Article()
article2.article_id = "2345"
article2.article_name = "test2"
article2.article_type = "0"
article2.article_quantity = "2"
article2.article_price_net = "250"
article2.article_price_gross = "275"
obj.add_article(article2)

xmlstr = ET.tostring(obj.build(), encoding='utf8', method='xml').decode()
print("\nXML Sent: {}".format(xmlstr))

headers = {'Content-Type': 'application/xml/'}
r = requests.post('https://test-api.billpay.de/v2/xml/offline/preauthorize', data=xmlstr, headers=headers)
print("\nResponse Received: {}".format(r.text))

if r.status_code == 200:
    response = PreauthorizeResponse(r.text)
    print("\nThe response:\n{}".format(response))
