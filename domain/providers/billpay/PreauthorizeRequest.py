from DefaultRequest import DefaultRequest, ET
from CommonNodes import BillpayNode, CustomerRestriction, InvoiceBankAccount, PaylaterDetailsNode
from typing import Optional


class CustomerDetails:
    GUEST = 'g'
    EXISTING_CUSTOMER = 'e'
    NEW_CUSTOMER = 'n'
    
    GROUP_BUSINESS = 'b'
    GROUP_PRIVATE = 'p'
    
    def __init__(self):
        self.customer_id = ''
        self.customer_type = ''
        self.salutation = ''
        self.title = ''
        self.first_name = ''
        self.last_name = ''
        self.street = ''
        self.street_no = ''
        self.address_addition = ''
        self.zip = ''
        self.city = ''
        self.country = ''
        self.email = ''
        self.phone = ''
        self.cell_phone = ''
        self.birthday = ''
        self.language = ''
        self.ip = ''
        self.customer_group = ''

        @property
        def customer_type(self) -> str:
            return self.customer_type

        @customer_type.setter
        def customer_type(self, value: str):
            if value not in [CustomerDetails.EXISTING_CUSTOMER, CustomerDetails.GUEST, CustomerDetails.NEW_CUSTOMER]:
                raise ValueError('Wrong customer type provided')

            self.customer_type = value

        @property
        def customer_group(self) -> str:
            return self.customer_group

        @customer_group.setter
        def customer_group(self, value: str):
            self.customer_group = value

    def build(self):
        return {
            'customerid': str(self.customer_id),
            'customertype': str(self.customer_type),
            'salutation': str(self.salutation),
            'title': str(self.title),
            'firstname': str(self.first_name),
            'lastname': str(self.last_name),
            'street': str(self.street),
            'streetnumber': str(self.street_no),
            'city': str(self.city),
            'country': str(self.country),
            'email': str(self.email),
            'phone': str(self.phone),
            'zipcode': str(self.zip),
            'cellphone': str(self.cell_phone),
            'dateofbirth': str(self.birthday),
            'language': str(self.language),
            'ipaddress': str(self.ip),
            'customergroup': str(self.customer_group),
        }


class ShippingDetails:
    def __init__(self):
        self.use_billing_address = 1
        self.salutation = ""
        self.title = ""
        self.first_name = ""
        self.last_name = ""
        self.street = ""
        self.street_number = ""
        self.addressaddition = ""
        self.zipcode = ""
        self.city = ""
        self.country = ""
        self.phone = ""
        self.cellphone = ""

    def build(self):
        if self.use_billing_address == 1:
            return {'usebillingaddress' : "1"}

        return { key.replace("_", ""):str(value) for key,value in self.__dict__.items()}


class CompanyDetails(BillpayNode):
    def __init__(self):
        self.name = ""
        self.legal_form = ""
        self.register_number = ""
        self.holder_name = ""
        self.tax_number = ""


class Article(BillpayNode):
    def __init__(self):
        self.article_id = ""
        self.article_name = ""
        self.article_type = 0
        self.article_quantity = 0
        self.article_price_net = 0
        self.article_price_gross = 0
        self.article_category = ""
        self.article_sub_category1 = ""
        self.article_sub_category2 = ""


class BankAccount(BillpayNode):
    def __init__(self):
        self.account_holder = ''
        self.account_number = ''
        self.sort_code = ''


class Total(BillpayNode):
    def __init__(self):
        self.shipping_name = ''
        self.shipping_price_net = 0
        self.shipping_price_gross = 0
        self.rebate_net = 0
        self.rebate_gross = 0
        self.order_amount_net = 0
        self.order_amount_gross = 0
        self.currency = ''
        self.reference = ''
        self.merchant_invoice_number = ''
        self.tracking_number = ''


class FraudDetection(BillpayNode):
    def __init__(self):
        self.session_id = ''


class RateRequest(BillpayNode):
    def __init__(self):
        self.rate_count = ''
        self.termin_months = ''
        self.total_amount_gross = ''

class AsyncRequest():
    def __init__(self):
        self.redirect_url = ""
        self.notify_url = ""

    def build(self):
        return self.__dict__.items()


class PreauthorizeRequest(DefaultRequest):
    INVOICE = 1
    DIRECT_DEBIT = 2
    TRANSACTION_CREDIT = 3
    PAYLATER = 4
    
    CAPTURE_AUTO = 0
    CAPTURE_MANUAL = 1
    
    TERMS_AND_CONDITIONS_ACCEPTED = 1
    TERMS_AND_CONDITIONS_NOT_ACCEPTED = 0
    
    ORIGIN_UNKNOWN = 'u'
    ORIGIN_ONLINE_SHOP = 'o'
    ORIGIN_OFFLINE = 'p'
    ORIGIN_TELESALES = 't'

    def __init__(self):
        super().__init__()
        self._request_type = "PREAUTHORIZE"
        
        self._customer_details = CustomerDetails()
        self._shipping_details = ShippingDetails()
        self._total = Total()
        self._company_details = None
        self._rate_request = None
        self._fraud_detection = None
        self._bank_account = None
        self._articles = []

        self.type_capture = PreauthorizeRequest.CAPTURE_MANUAL
        self.origin_of_sale = PreauthorizeRequest.ORIGIN_ONLINE_SHOP
        self.payment_type = PreauthorizeRequest.INVOICE
        self.terms_accepted = PreauthorizeRequest.TERMS_AND_CONDITIONS_ACCEPTED
        self.expected_day_shipping = "0"

    @property
    def bank_account(self) -> Optional[BankAccount]:
        return self._bank_account

    @bank_account.setter
    def bank_account(self, value: BankAccount):
        self._bank_account = value

    @property
    def company_details(self) -> Optional[CompanyDetails]:
        return self._company_details

    @company_details.setter
    def company_details(self, value: CompanyDetails):
        self._company_details = value

    @property
    def rate_request(self) -> Optional[RateRequest]:
        return self._rate_request

    @rate_request.setter
    def rate_request(self, value: RateRequest):
        self._rate_request = value

    @property
    def fraud_detection(self) -> Optional[FraudDetection]:
        return self._fraud_detection

    @fraud_detection.setter
    def fraud_detection(self, value: FraudDetection):
        self._fraud_detection = value

    @property
    def customer_details(self) -> CustomerDetails:
        return self._customer_details

    @customer_details.setter
    def customer_details(self, value: CustomerDetails):
        self._customer_details = value

    @property
    def shipping_details(self) -> ShippingDetails:
        return self._shipping_details

    @shipping_details.setter
    def shipping_details(self, value : ShippingDetails):
        self._shipping_details = value

    @property
    def total(self) -> Total:
        return self._total

    @total.setter
    def total(self, value : Total):
        self._total = value

    def add_article(self, value : Article):
        self._articles.append(value)

    def build(self):
        self.params['requesttype'] = str(self._request_type)
        self.params['tcaccepted'] = str(self.terms_accepted)
        self.params['expecteddaystillshipping'] = str(self.expected_day_shipping)
        self.params['manualcapture'] = str(self.type_capture)
        self.params['paymenttype'] = str(self.payment_type)
        self.params['originofsale'] = str(self.origin_of_sale)

        data = super().build()

        ET.SubElement(data, "customer_details", self._customer_details.build()) 
        
        if self._company_details is not None:
            ET.SubElement(data, "company_details", self._company_details.build())
        
        ET.SubElement(data, "shipping_details", self._shipping_details.build())
        ET.SubElement(data, "total", self._total.build())

        article_node = ET.SubElement(data, "article_data")
        for article in self._articles:
            ET.SubElement(article_node, "article", article.build())

        if self._bank_account is not None:
            ET.SubElement(data, "bank_account", self._bank_account.build())

        if self._fraud_detection is not None:
            ET.SubElement(data, "fraud_detection", self._fraud_detection.build())

        if self._rate_request is not None:
            ET.SubElement(data, "rate_request", self._rate_request.build())

        return data


def preauthorize(xml: str):
    root = ET.fromstring(xml)
    error_code = int(root.attrib['errorcode'])

    if error_code == 0:
        return PreauthorizeResponse(root)
    else:
        return ErrorResponse(root)


class ErrorResponse:
    def __init__(self, root: ET):
        self.customer_message = root.attrib['customermessage']
        self.developer_message = root.attrib['developermessage']
        self.error_code = int(root.attrib['errorcode'])
        self.merchant_message = root.attrib['merchantmessage']
        self.response_type = root.attrib['responsetype']

    def __str__(self):
        return ('ErrorReponse(\n'
                'customer_message: {customer_message}\n'
                'developer_message: {developer_message}\n'
                'error_code: {error_code}\n'
                'merchant_message: {merchant_message}\n'
                'response_type: {response_type}'
                ')\n').format(**self.__dict__)


class PreauthorizeResponse():
    def __init__(self, root: ET):
        self.response_type = root.attrib['responsetype']
        self.error_code = int(root.attrib['errorcode'])
        self.status = root.attrib['status']
        self.transaction_id = root.attrib['transactionid']
        self.customer_restriction = CustomerRestriction(root)

        invoice_bank_account = root.find('./invoice_bank_account')
        self.invoice_bank_account = InvoiceBankAccount(root) if invoice_bank_account else None

        instalment_details = root.find('./instalment_details')
        self.instalment_details = PaylaterDetailsNode(instalment_details) if instalment_details else None

        corrected_address_node = root.find('./corrected_address')
        self.corrected_address = CorrectedAddress(corrected_address_node) if corrected_address_node else None

    def __str__(self):
        return ('PreauthorizeResponse(\n'
                'error_code: {error_code}\n'
                'response_type: {response_type}\n'
                'status: {status}\n'
                'transaction_id: {transaction_id}\n'
                'invoice_bank_account: {invoice_bank_account}\n'
                'customer_restriction: {customer_restriction}\n'
                'corrected_address: {corrected_address})\n'
                'instalment_details: {instalment_details})\n'
                ).format(**self.__dict__)


class CorrectedAddress:
    def __init__(self, corrected_address_node: ET):
        self.city = corrected_address_node.attrib['city']
        self.country = corrected_address_node.attrib['country']
        self.street = corrected_address_node.attrib['street']
        self.street_number = corrected_address_node.attrib['streetnumber']
        self.zipcode = corrected_address_node.attrib['zipcode']

    def __str__(self):
        return ('CorrectedAddress(\n'
                'city: {city}\n'
                'country: {country}\n'
                'street: {street}\n'
                'street_number: {street_number}\n'
                'zipcode: {zipcode})\n'
                ).format(**self.__dict__)