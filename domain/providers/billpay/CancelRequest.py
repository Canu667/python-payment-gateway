from DefaultRequest import DefaultRequest, DefaultResponse, ET


class CancelRequest(DefaultRequest):

    TYPE = "CANCEL"

    def __init__(self, reference: str, order_amount_gross: int, currency: str):
        super().__init__()

        self.order_amount_gross = str(order_amount_gross)
        self.currency = currency
        self.reference = reference

        self.params['requesttype'] = self.TYPE

    def get_request_endpoint(self) -> str:
        return '/cancel'

    def build(self):
        data = super().build()

        ET.SubElement(data, "cancel_params", {
            "orderamountgross": self.order_amount_gross,
            "currency": self.currency,
            "reference": self.reference,
        })
        return data


class CancelResponse(DefaultResponse):
    def __init__(self, root: ET):
        super().__init__(root)

        self.customer_message = root.attrib['customermessage']
        self.developer_message = root.attrib['developermessage']
        self.merchant_message = root.attrib['merchantmessage']
        self.error_code = int(root.attrib['errorcode'])
        self.response_type = root.attrib['responsetype']

    def __str__(self):
        return ('CancelResponse(\n'
                'error_code: {error_code}\n)'
                ).format(**self.__dict__)
