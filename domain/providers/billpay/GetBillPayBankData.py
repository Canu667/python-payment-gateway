from DefaultRequest import DefaultRequest, ET


class GetBillPayBankData(DefaultRequest):
    def __init__(self, order_ref):
        super().__init__()
        self._requesttype = "GET_BILLPAY_BANK_DATA"
        self._order_ref = order_ref

    def build(self):
        data = super().build()
        ET.SubElement(data, "order_params", reference=self._order_ref)

        return data
