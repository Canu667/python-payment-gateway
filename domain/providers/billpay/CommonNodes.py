class CustomerRestriction:
    def __init__(self, root: ET):
        customer_restriction_node = root.find('./customer_restriction')
        self.shippingtypeobligation = customer_restriction_node.attrib['shippingtypeobligation']
    def __str__(self):
        return ('CustomerRestriction(shippingtypeobligation: {shippingtypeobligation}'
                ).format(**self.__dict__)