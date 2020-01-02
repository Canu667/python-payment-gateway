from marshmallow import Schema, fields


class PaymentSchema(Schema):
    payment_method = fields.String(required=True, data_key='paymentMethod')
    order_id = fields.String(required=True, data_key='orderId')
    amount = fields.Int(required=True)
    # customer = fields.Nested(
    #    CustomerSchema, attribute='customer', dump_only=True)
