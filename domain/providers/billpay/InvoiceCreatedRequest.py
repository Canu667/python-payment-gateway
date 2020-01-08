from DefaultRequest import DefaultRequest, ET
from CommonNodes import InvoiceBankAccount


class InvoiceCreatedRequest(DefaultRequest):
    PARTIAL_ACTIVATION = 1
    FULL_ACTIVATION = 0

    def __init__(self, invoice_amount_gross: int, currency: str, reference: str, delivery_delay_in_days: int):
        super().__init__()
        self._request_type = "INVOICE_CREATED"

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


class InvoiceCreatedResponse():
    def __init__(self, xml: str):
        root = ET.fromstring(xml)

        self.customer_message = root.attrib['customermessage']
        self.developer_message = root.attrib['developermessage']
        self.merchant_message = root.attrib['merchantmessage']
        self.error_code = int(root.attrib['errorcode'])
        self.response_type = root.attrib['responsetype']

        valid_response = self.is_successful()

        if valid_response and root.find('./invoice_bank_account') is not None:
            self.invoice_bank_account = InvoiceBankAccount(root)
        else:
            self.invoice_bank_account = None

    def is_successful(self):
        return True if self.error_code == 0 else False