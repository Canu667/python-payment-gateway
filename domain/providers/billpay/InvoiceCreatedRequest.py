from .DefaultRequest import DefaultRequest, DefaultResponse, ET
from .CommonNodes import InvoiceBankAccount, PaylaterDetailsNode


class InvoiceCreatedRequest(DefaultRequest):
    PARTIAL_ACTIVATION = 1
    FULL_ACTIVATION = 0

    TYPE = "INVOICE_CREATED"

    def __init__(self, invoice_amount_gross: int, currency: str, reference: str, delivery_delay_in_days: int):
        super().__init__()
        self.params['requesttype'] = self.TYPE

        self.invoice_amount_net = None
        self.invoice_amount_gross = invoice_amount_gross
        self.is_partial = InvoiceCreatedRequest.FULL_ACTIVATION

        self.rebate_net = None
        self.rebate_gross = None
        self.shipping_name = None
        self.shipping_price_net = None
        self.shipping_price_gross = None
        self.currency = currency
        self.reference = reference
        self.merchant_invoice_number = None
        self.tracking_number = None
        self.delivery_delay_in_days = delivery_delay_in_days

    def get_request_endpoint(self) -> str:
        return '/invoiceCreated'

    def build(self):
        data = super().build()

        ET.SubElement(data, "invoice_params", {
            key.replace("_", ""): str(value)
            for key, value in self.__dict__.items()
            if key in [
                'invoice_amount_net',
                'invoice_amount_gross',
                'is_partial',
                'rebate_net',
                'rebate_gross',
                'shipping_name',
                'shipping_price_net',
                'shipping_price_gross',
                'currency',
                'reference',
                'merchant_invoice_number',
                'tracking_number',
                'delivery_delay_in_days'
            ] and value is not None
        })

        return data


class InvoiceCreatedResponse(DefaultResponse):
    def __init__(self, root: ET):
        super().__init__(root)
        invoice_bank_account = root.find('./invoice_bank_account')
        self.invoice_bank_account = InvoiceBankAccount(root) if invoice_bank_account else None

        instalment_details = root.find('./instalment_details')
        self.instalment_details = PaylaterDetailsNode(instalment_details) if instalment_details else None