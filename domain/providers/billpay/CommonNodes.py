import xml.etree.cElementTree as ET


class BillpayNode:
    def build(self):
        return { key.replace("_", ""): str(value) for key, value in self.__dict__.items()}


class CustomerRestriction:
    def __init__(self, root: ET):
        customer_restriction_node = root.find('./customer_restriction')
        self.shipping_type_obligation = customer_restriction_node.attrib['shippingtypeobligation']

    def __str__(self):
        return ('CustomerRestriction(shipping_type_obligation: {shipping_type_obligation}'
                ).format(**self.__dict__)


class InvoiceBankAccount:
    def __init__(self, root: ET):
        invoice_bank_account_node = root.find('./invoice_bank_account')

        self.account_holder = invoice_bank_account_node.attrib['accountholder']
        self.account_number = invoice_bank_account_node.attrib['accountnumber']
        self.activation_performed = invoice_bank_account_node.attrib['activationperformed']
        self.bank_code = invoice_bank_account_node.attrib['bankcode']
        self.bank_name = invoice_bank_account_node.attrib['bankname']
        self.invoice_due_date = invoice_bank_account_node.attrib['invoiceduedate']
        self.invoice_reference = invoice_bank_account_node.attrib['invoicereference']

    def __str__(self):
        return ('InvoiceBankAccount(\n'
                'account_holder: {account_holder}\n'
                'account_number: {account_number}\n'
                'activation_performed: {activation_performed}\n'
                'bank_code: {bank_code}\n'
                'bank_name: {bank_name}\n'
                'invoice_due_date: {invoice_due_date}\n'
                'invoice_reference: {invoice_reference})\n'
                ).format(**self.__dict__)


class PaylaterDetailsNode:
    def __init__(self, instalment_details_node: ET):
        instl_plan_node = instalment_details_node.find('./instl_plan')

        self.number_of_instalments = instl_plan_node.attrib['numinst']

        calc_node = instalment_details_node.find('./calc')

        if calc_node is not None:
            self.duration_in_months = calc_node.attrib['duration_in_months']
            self.fee_percent = calc_node.attrib['fee_percent']
            self.fee_total = calc_node.attrib['fee_total']
            self.total_payment = calc_node.attrib['total_pymt']
            self.eff_anual = calc_node.attrib['eff_anual']
            self.nominal = calc_node.attrib['nominal']

        instl_list_nodes = instl_plan_node.find('./instl_list')
        self.instalments = [
            {
                'date': instalment.attrib['date'],
                'type': instalment.attrib['type'],
                'text': instalment.text
            }
            for instalment in instl_list_nodes.iter('instl')
        ] if instl_list_nodes is not None else []

    def __str__(self):
        return ('PaylaterDetailsNode(number_of_instalments: {number_of_instalments}, instalments: {instalments}'
                ).format(**self.__dict__)