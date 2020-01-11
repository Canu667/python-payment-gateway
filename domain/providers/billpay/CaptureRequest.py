from DefaultRequest import DefaultRequest, DefaultResponse, ET
from CommonNodes import InvoiceBankAccount


class CaptureRequest(DefaultRequest):

    TYPE = "CAPTURE"

    def __init__(self, transaction_id: str, order_amount_gross: int, currency: str, reference: str):
        super().__init__()
        self.transaction_id = transaction_id
        self.order_amount_gross = str(order_amount_gross)
        self.currency = currency
        self.reference = reference
        self.merchant_invoice_number = ''
        self.customer_id = ''

        self.params['requesttype'] = self.TYPE

    def get_request_endpoint(self) -> str:
        return '/capture'

    def build(self):
        data = super().build()

        ET.SubElement(data, "capture_params", {
            "transactionid": str(self.transaction_id),
            "orderamountgross": str(self.order_amount_gross),
            "currency": str(self.currency),
            "reference": str(self.reference),
            "merchantinvoicenumber": str(self.merchant_invoice_number),
            "customerid": str(self.customer_id),
        })
        return data


class CaptureResponse(DefaultResponse):
    def __init__(self, root: ET):
        super().__init__(root)

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

        if valid_response and root.find('./assigned_invoice_number') is not None:
            self.invoice_bank_account = InvoiceNumbers(root)
        else:
            self.invoice_bank_account = None

    def is_successful(self):
        return True if self.error_code == 0 else False


class InvoiceNumbers:
    def __init__(self, root: ET):
        assigned_invoice_number_node = root.find('./assigned_invoice_number')
        invoice_number_node = assigned_invoice_number_node.find('./invoice_number')

        self.invoice_id = invoice_number_node.attrib['invoiceid']
        self.billpay_invoice_number = invoice_number_node.attrib['billpayinvoicenumber']

    def __str__(self):
        return ('InvoiceNumbers(invoiceid: {invoiceid}, billpayinvoicenumber: {billpayinvoicenumber}'
                ).format(**self.__dict__)


class TransactionCredit:
    def __init__(self, root: ET):
        option_node = root.find('./option')

        self.rate_count = option_node.attrib['ratecount']
        self.termin_months = option_node.attrib['terminmonths']

        calculation_node = root.find('./calculation')
        self.base = calculation_node.find('./base').text