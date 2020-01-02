from DefaultRequest import DefaultRequest, ET

class CustomerDetails:
    GUEST = 'g'
    EXISTING_CUSTOMER = 'e'
    NEW_CUSTOMER = 'n'

    def __init__(self):
        self.customer_id = ''
        self.customer_type = ''
        self.salutation = ''
        self.title = ''
        self.firstname = ''
        self.lastname = ''
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
            'firstname': str(self.firstname),
            'lastname': str(self.lastname),
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
        self.usebillingaddress = 1
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
        if self.usebillingaddress == 1:
            return {'usebillingaddress' : "1"}

        return { key.replace("_", ""):str(value) for key,value in self.__dict__.items()}

class BillpayNode:
    def build(self):
        return { key.replace("_", ""):str(value) for key,value in self.__dict__.items()}

class CompanyDetails(BillpayNode):
    def __init__(self):
        self.name = ""
        self.legalform = ""
        self.registernumber = ""
        self.holdername = ""
        self.taxnumber = ""

class Article(BillpayNode):
    def __init__(self):
        self.articleid = ""
        self.articlename = ""
        self.articletype = 0
        self.articlequantity = 0
        self.articlepricenet = 0
        self.articlepricegross = 0
        self.articlecategory = ""
        self.articlesubcategory1 = ""
        self.articlesubcategory2 = ""

class BankAccount(BillpayNode):
    def __init__(self):
        self.accountholder = ''
        self.accountnumber = ''
        self.sortcode = ''

class Total(BillpayNode):
    def __init__(self):
        self.shippingname = ''
        self.shippingpricenet = 0
        self.shippingpricegross = 0
        self.rebatenet = 0
        self.rebategross = 0
        self.orderamountnet = 0
        self.orderamountgross = 0
        self.currency = ''
        self.reference = ''
        self.merchantinvoicenumber = ''
        self.trackingnumber = ''

class FraudDetection(BillpayNode):
    def __init__(self):
        self.sessionid = ''

class RateRequest(BillpayNode):
    def __init__(self):
        self.ratecount = ''
        self.terminmonths = ''
        self.totalamountgross = ''

class AsyncRequest():
    def __init__(self):
        self.redirect_url = ""
        self.notify_url = ""

    def build(self):
        return self.__dict__.items()

class PreauthorizeRequest(DefaultRequest):
    INVOICE = 'invoice'

    def __init__(self, payment_method: str):
        super().__init__()
        self._requesttype = "PREAUTHORIZE"

        if payment_method not in [PreauthorizeRequest.INVOICE]:
            raise ValueError("Payment method {} for Billpay not recognised".format(payment_method))

        self._payment_method = payment_method
        self.customer_details = None
        self.shipping_details = ShippingDetails()
        self.total = None
        self._articles = []
        self.params['requesttype'] = self._requesttype
        self.params['tcaccepted'] = "1"
        self.params['expecteddaystillshipping'] = "0"
        self.params['manualcapture'] = "0"
        self.params['paymenttype'] = "1"
        self.params['originofsale'] = "o"

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
        data = super().build()

        ET.SubElement(data, "customer_details", self._customer_details.build())
        ET.SubElement(data, "shipping_details", self._shipping_details.build())
        ET.SubElement(data, "total", self._total.build())

        article_node =  ET.SubElement(data, "article_data")
        for article in self._articles:
            ET.SubElement(article_node, "article", article.build())

        return data

class PreauthorizeResponse:
    def __init__(self, xml: str):
        root = ET.fromstring(xml)

        self.customer_message = root.attrib['customermessage']
        self.developer_message = root.attrib['developermessage']
        self.errorcode = int(root.attrib['errorcode'])
        self.merchantmessage = root.attrib['merchantmessage']
        self.responsetype = root.attrib['responsetype']

        valid_response = True if self.errorcode == 0 else False

        self.status = root.attrib['status'] if valid_response else None
        self.transactionid = root.attrib['transactionid'] if valid_response else None
        self.invoice_bank_account = InvoiceBankAccount(root) if valid_response else None
        self.customer_restriction = CustomerRestriction(root) if valid_response else None

        self.corrected_address = CorrectedAddress(root)

    def __str__(self):
        return ('PreauthorizeResponse(\n'
                'customer_message: {customer_message}\n'
                'developer_message: {developer_message}\n'
                'errorcode: {errorcode}\n'
                'merchantmessage: {merchantmessage}\n'
                'responsetype: {responsetype}\n'
                'status: {status}\n'
                'transactionid: {transactionid}\n'
                'invoice_bank_account: {invoice_bank_account}\n'
                'customer_restriction: {customer_restriction}\n'
                'corrected_address: {corrected_address})\n'
                ).format(**self.__dict__)

class CorrectedAddress:
    def __init__(self, root: ET):
        corrected_address_node = root.find('./corrected_address')
        self.city = corrected_address_node.attrib['city']
        self.country = corrected_address_node.attrib['country']
        self.street = corrected_address_node.attrib['street']
        self.streetnumber = corrected_address_node.attrib['streetnumber']
        self.zipcode = corrected_address_node.attrib['zipcode']
    def __str__(self):
        return ('CorrectedAddress(\n'
                'city: {city}\n'
                'country: {country}\n'
                'street: {street}\n'
                'streetnumber: {streetnumber}\n'
                'zipcode: {zipcode})\n'
                ).format(**self.__dict__)

class InvoiceBankAccount:
    def __init__(self, root: ET):
        invoice_bank_account_node = root.find('./invoice_bank_account')
        self.accountholder = invoice_bank_account_node.attrib['accountholder']
        self.accountnumber = invoice_bank_account_node.attrib['accountnumber']
        self.activationperformed = invoice_bank_account_node.attrib['activationperformed']
        self.bankcode = invoice_bank_account_node.attrib['bankcode']
        self.bankname = invoice_bank_account_node.attrib['bankname']
        self.invoiceduedate = invoice_bank_account_node.attrib['invoiceduedate']
        self.invoicereference = invoice_bank_account_node.attrib['invoicereference']
    def __str__(self):
        return ('InvoiceBankAccount(\n'
                'accountholder: {accountholder}\n'
                'accountnumber: {accountnumber}\n'
                'activationperformed: {activationperformed}\n'
                'bankcode: {bankcode}\n'
                'bankname: {bankname}\n'
                'invoiceduedate: {invoiceduedate}\n'
                'invoicereference: {invoicereference})\n'
                ).format(**self.__dict__)

class CustomerRestriction:
    def __init__(self, root: ET):
        customer_restriction_node = root.find('./customer_restriction')
        self.shippingtypeobligation = customer_restriction_node.attrib['shippingtypeobligation']
    def __str__(self):
        return ('CustomerRestriction(shippingtypeobligation: {shippingtypeobligation}'
                ).format(**self.__dict__)