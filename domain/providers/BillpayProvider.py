from domain.providers.provider import (
    Provider,
    CouldNotInitialisePayment,
    CouldNotCaptureOnPayment,
    CouldNotActivatePayment
)
from schemas.payment import PaymentDto
from domain.providers.billpay.BillpayClient import BillpayClient
from domain.providers.billpay.PreauthorizeRequest import (
    PreauthorizeRequest,
    PreauthorizeResponse,
    CustomerDetails,
    Total,
    Article
)
from domain.providers.billpay.CaptureRequest import CaptureRequest, CaptureResponse
from domain.providers.billpay.InvoiceCreatedRequest import InvoiceCreatedRequest, InvoiceCreatedResponse
from domain.providers.billpay.DefaultRequest import ErrorResponse
from models.payment_model import PaymentModel


class BillpayProvider(Provider):
    def __init__(self, private_client: BillpayClient, business_client: BillpayClient):
        self.private_client = private_client
        self.business_client = business_client

    def create_payment(self, payment: PaymentDto) -> PreauthorizeResponse:
        obj = PreauthorizeRequest()
        obj.type_capture = PreauthorizeRequest.CAPTURE_MANUAL

        customer_details = CustomerDetails()
        customer_details.customer_type = CustomerDetails.EXISTING_CUSTOMER
        customer_details.salutation = "Herr"
        customer_details.first_name = payment.billing_address.first_name
        customer_details.last_name = payment.billing_address.last_name
        customer_details.street = payment.billing_address.street
        customer_details.street_no = payment.billing_address.street_number
        customer_details.zip = payment.billing_address.zip
        customer_details.city = payment.billing_address.city
        customer_details.country = payment.billing_address.country.iso2
        customer_details.email = payment.customer.email
        customer_details.phone = payment.customer.phone
        customer_details.cell_phone = payment.customer.mobile_phone
        customer_details.birthday = payment.customer.birthday
        customer_details.language = "de"
        customer_details.ip = payment.customer.ip
        customer_details.customer_group = CustomerDetails.GROUP_PRIVATE
        obj.customer_details = customer_details

        total = Total()
        total.shipping_name = payment.shipping.name
        total.shipping_price_net = payment.shipping.net_amount
        total.shipping_price_gross = payment.shipping.gross_amount
        total.rebate_net = payment.order.discount_net_amount
        total.rebate_gross = payment.order.discount_gross_amount
        total.order_amount_net = payment.order.net_amount
        total.order_amount_gross = payment.order.gross_amount
        total.currency = "EUR"
        total.reference = payment.reference_id
        obj.total = total

        for item in payment.order.items:
            article = Article()
            article.article_id = item.id
            article.article_name = item.name
            article.article_type = item.type
            article.article_quantity = item.quantity
            article.article_price_net = item.net_amount
            article.article_price_gross = item.gross_amount
            obj.add_article(article)

        response = self.private_client.preauthorise(obj)

        if isinstance(response, ErrorResponse):
            raise CouldNotInitialisePayment(payment.reference_id, response.merchant_message)

        return response

    def capture(self, payment: PaymentModel):
        obj = CaptureRequest(payment.transaction_id, payment.amount, "EUR", payment.reference_id)

        response = self.private_client.capture(obj)

        if isinstance(response, ErrorResponse):
            raise CouldNotCaptureOnPayment(payment.reference_id, response.merchant_message)

        return response

    def create_invoice(self, payment: PaymentModel):
        obj = InvoiceCreatedRequest(payment.amount, "EUR", payment.reference_id, 1)
        response = self.private_client.create_invoice(obj)

        if isinstance(response, ErrorResponse):
            raise CouldNotActivatePayment(payment.reference_id, response.merchant_message)

        return response
