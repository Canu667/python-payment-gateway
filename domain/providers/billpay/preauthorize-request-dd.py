from PreauthorizeRequest import PreauthorizeRequest, BankAccount, PreauthorizeResponse, CustomerDetails, Total, Article
import xml.etree.cElementTree as ET
import requests
import os

obj = PreauthorizeRequest()

obj.mid = os.environ['BILLPAY_MERCHANT_ID']
obj.pid = os.environ['BILLPAY_PORTAL_ID']
obj.password_hash = os.environ['BILLPAY_PASSWORD_HASH']
obj.payment_type = PreauthorizeRequest.DIRECT_DEBIT

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
customer_details.customer_group = CustomerDetails.GROUP_PRIVATE
obj.customer_details = customer_details

bank_account = BankAccount()
bank_account.account_holder = "Thomas Testkunde"
bank_account.account_number = "DE12500105170648489890"
obj.bank_account = bank_account

total = Total()
total.shipping_name = "Express-Versand"
total.shipping_price_net = 500
total.shipping_price_gross = 650
total.rebate_net = 0
total.rebate_gross = 0
total.order_amount_net = 1250
total.order_amount_gross = 1475
total.currency = "EUR"
total.reference = "0000001"
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
