from domain.providers.provider import Provider, CouldNotInitialisePayment
from models.payment import Payment
from domain.providers.billpay.BillpayClient import BillpayClient
from domain.providers.billpay.PreauthorizeRequest import (
    PreauthorizeRequest,
    CustomerDetails,
    Total,
    Article
)
from domain.providers.billpay.DefaultRequest import ErrorResponse


class BillpayProvider(Provider):
    def __init__(self, private_client: BillpayClient, business_client: BillpayClient):
        self.private_client = private_client
        self.business_client = business_client

    def create_payment(self, payment: Payment) -> None:
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
        total.reference = payment.order_id
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

        response = self.private_client.preauthorise(obj)

        if isinstance(response, ErrorResponse):
            raise CouldNotInitialisePayment(payment.order_id, response.merchant_message)

