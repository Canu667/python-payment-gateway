from DefaultRequest import DefaultRequest, ET
from CommonNodes import InvoiceBankAccount, PaylaterDetailsNode


class InvoiceCreatedRequest(DefaultRequest):
    PARTIAL_ACTIVATION = 1
    FULL_ACTIVATION = 0

    def __init__(self, invoice_amount_gross: int, currency: str, reference: str, delivery_delay_in_days: int):
        super().__init__()
        self.params['requesttype'] = "INVOICE_CREATED"

        self.invoice_amount_net = 0
        self.invoice_amount_gross = invoice_amount_gross
        self.is_partial = 0

        self.rebate_net = 0
        self.rebate_gross = 0
        self.shipping_name = ""
        self.shipping_price_net = ""
        self.shipping_price_gross = ""
        self.currency = currency
        self.reference = reference
        self.merchant_invoice_number = ""
        self.tracking_number = ""
        self.delivery_delay_in_days = delivery_delay_in_days

    def build(self):
        data = super().build()

        ET.SubElement(data, "invoice_params", {
            "invoiceamountnet": str(self.invoice_amount_net),
            "invoiceamountgross": str(self.invoice_amount_gross),
            "ispartial": str(self.is_partial),
            "rebatenet": str(self.rebate_net),
            "rebategross": str(self.rebate_gross),
            "shippingname": str(self.shipping_name),
            "shippingpricenet": str(self.shipping_price_net),
            "shippingpricegross": str(self.shipping_price_gross),
            "currency": str(self.currency),
            "reference": str(self.reference),
            "merchantinvoicenumber": str(self.merchant_invoice_number),
            "trackingnumber": str(self.tracking_number),
            "deliverydelayindays": str(self.delivery_delay_in_days),
        })
        return data


def create_response(xml: str):
    root = ET.fromstring(xml)
    error_code = int(root.attrib['errorcode'])

    if error_code == 0:
        return InvoiceCreatedResponse(root)
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


class InvoiceCreatedResponse():
    def __init__(self, root: ET):
        invoice_bank_account = root.find('./invoice_bank_account')
        self.invoice_bank_account = InvoiceBankAccount(root) if invoice_bank_account else None

        instalment_details = root.find('./instalment_details')
        self.instalment_details = PaylaterDetailsNode(instalment_details) if instalment_details else None