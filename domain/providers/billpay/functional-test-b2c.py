from PreauthorizeRequest import PreauthorizeRequest, CustomerDetails, Total, Article
from CaptureRequest import CaptureRequest
from BillpayClient import BillpayClient
from InvoiceCreatedRequest import InvoiceCreatedRequest
from CancelRequest import CancelRequest
import os
import sys
import time

manager = BillpayClient(
    mid=os.environ['BILLPAY_MERCHANT_ID'],
    pid=os.environ['BILLPAY_PORTAL_ID'],
    password_hash=os.environ['BILLPAY_PASSWORD_HASH']
)
customer_reference = str(int(time.time())) + "TEST"
print("Reference used: {}".format(customer_reference))

obj = PreauthorizeRequest()
obj.type_capture = PreauthorizeRequest.CAPTURE_MANUAL

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

total = Total()
total.shipping_name = "Express-Versand"
total.shipping_price_net = 500
total.shipping_price_gross = 650
total.rebate_net = 0
total.rebate_gross = 0
total.order_amount_net = 1250
total.order_amount_gross = 1475
total.currency = "EUR"
total.reference = customer_reference
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

response = manager.preauthorise(obj)
print("\nThe response:\n{}".format(response))

if response.is_successful() is not True:
    print("Ending the test")
    sys.exit()

obj = CaptureRequest(response.transaction_id, 1475, "EUR", customer_reference)

response = manager.capture(obj)
print("\nThe response:\n{}".format(response))

if response.is_successful() is not True:
    print("Ending the test")
    sys.exit()

obj = InvoiceCreatedRequest(1475, "EUR", customer_reference, 1)
obj.invoice_amount_net = 1250
obj.invoice_amount_gross = 1475
obj.shipping_name = "Express-Versand"
obj.shipping_price_net = 500
obj.shipping_price_gross = 650

response = manager.create_invoice(obj)
print("\nThe response:\n{}".format(response))

if response.is_successful() is not True:
    print("Ending the test")
    sys.exit()

obj = CancelRequest(customer_reference, 1475, "EUR")
response = manager.cancel(obj)
print("\nThe response:\n{}".format(response))