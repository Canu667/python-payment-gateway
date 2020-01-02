from PreauthorizeRequest import PreauthorizeRequest, PreauthorizeResponse, CustomerDetails, Total, Article
import xml.etree.cElementTree as ET
import requests
import os

obj = PreauthorizeRequest('invoice')

obj.mid = os.environ['BILLPAY_MERCHANT_ID']
obj.pid = os.environ['BILLPAY_PORTAL_ID']
obj.passwordhash = os.environ['BILLPAY_PASSWORD_HASH']

customer_details = CustomerDetails()
# customer_details.customer_id = 1714809
customer_details.customer_type = CustomerDetails.NEW_CUSTOMER
customer_details.salutation = "Herr"
customer_details.firstname = "Mateusz"
customer_details.lastname = "Canova"
# customer_details.title = "Dr."
customer_details.street = "Almstadtstr."
customer_details.street_no = "49"
customer_details.zip = "10119"
customer_details.city = "Berlin"
customer_details.country = "DEU"
customer_details.email = "matcan@wp.pl"
 # customer_details.phone = "0302333453"
customer_details.cell_phone = "01775112383"
customer_details.birthday = "19850112"
customer_details.language = "de"
customer_details.ip = "85.214.7.10"
customer_details.customer_group = "p"
obj.customer_details = customer_details

total = Total()
total.shippingname = "Express-Versand"
total.shippingpricenet = 500
total.shippingpricegross = 650
total.rebatenet = 0
total.rebategross = 0
total.orderamountnet = 1250
total.orderamountgross = 1475
total.currency = "EUR"
total.reference = "111114"
obj.total = total

article = Article()
article.articleid = "1234"
article.articlename = "test1"
article.articletype = "0"
article.articlequantity = "1"
article.articlepricenet = "250"
article.articlepricegross = "275"
obj.add_article(article)

article2 = Article()
article2.articleid = "2345"
article2.articlename = "test2"
article2.articletype = "0"
article2.articlequantity = "2"
article2.articlepricenet = "250"
article2.articlepricegross = "275"
obj.add_article(article2)

xmlstr = ET.tostring(obj.build(), encoding='utf8', method='xml').decode()
print(xmlstr)

headers = {'Content-Type': 'application/xml/'}
r = requests.post('https://test-api.billpay.de/v2/xml/offline/preauthorize', data=xmlstr, headers=headers)
print("\n")
print(r.text)
response = PreauthorizeResponse(r.text)
print(response)
