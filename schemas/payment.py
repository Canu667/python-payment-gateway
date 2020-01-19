from marshmallow_objects import Model, NestedModel, fields


class ReservedPaymentDto(Model):
    id = fields.Int(required=True, data_key='id')


class PaymentResponseDto(Model):
    id = fields.Int(required=True, data_key='id')
    payment_method = fields.String(required=True, data_key='payment_method')
    amount = fields.Int(required=True, data_key='amount')


class ItemSchema(Model):
    id = fields.Int(required=True, data_key='id')
    name = fields.String(required=True, data_key='name')
    type = fields.String(required=True, data_key='type')
    quantity = fields.Int(required=True, data_key='quantity')
    gross_amount = fields.Int(required=True, data_key='gross_amount')
    net_amount = fields.Int(required=True, data_key='net_amount')


class OrderSchema(Model):
    gross_amount = fields.Int(required=True, data_key='gross_amount')
    net_amount = fields.Int(required=True, data_key='net_amount')
    discount_gross_amount = fields.Int(required=True, data_key='discount_gross_amount')
    discount_net_amount = fields.Int(required=True, data_key='discount_net_amount')
    items = fields.List(
        NestedModel(ItemSchema)
    )


class ShippingSchema(Model):
    name = fields.String(required=True, data_key='name')
    gross_amount = fields.Int(required=True, data_key='gross_amount')
    net_amount = fields.Int(required=True, data_key='net_amount')


class CustomerSchema(Model):
    first_name = fields.String(required=True, data_key='first_name')
    last_name = fields.String(required=True, data_key='last_name')
    type = fields.String(required=True, data_key='type')
    email = fields.String(required=True, data_key='email')
    phone = fields.String(required=True, data_key='phone')
    mobile_phone = fields.String(required=True, data_key='mobile_phone')
    birthday = fields.String(required=True, data_key='birthday')
    ip = fields.String(required=True, data_key='ip')


class CountrySchema(Model):
    iso2 = fields.String(required=True, data_key='iso2')
    name = fields.String(required=True, data_key='name')


class AddressSchema(Model):
    first_name = fields.String(required=True, data_key='first_name')
    last_name = fields.String(required=True, data_key='last_name')
    company_name = fields.String(required=True, data_key='company_name')
    street = fields.String(required=True, data_key='street')
    street_number = fields.String(required=True, data_key='street_number')
    city = fields.String(required=True, data_key='city')
    zip = fields.String(required=True, data_key='zip')
    additional = fields.String(required=True, data_key='additional')
    country = NestedModel(CountrySchema, attribute='country')


class AuthorisationUrlSchema(Model):
    success_url = fields.String(required=True, data_key='success_url')
    error_url = fields.String(required=True, data_key='error_url')
    cancel_url = fields.String(required=True, data_key='cancel_url')


class PaymentConfiguration(Model):
    payment_method = fields.String(required=True, data_key='payment_method')
    authorisation_url = NestedModel(AuthorisationUrlSchema, attribute='authorisation_url')


class PaymentDto(Model):
    reference_id = fields.String(required=True, data_key='reference_id')
    currency = fields.String(required=True, data_key='currency')
    order = NestedModel(OrderSchema, attribute='order')
    shipping = NestedModel(ShippingSchema, attribute='shipping')
    customer = NestedModel(CustomerSchema, attribute='customer')
    billing_address = NestedModel(AddressSchema, attribute='billing_address')
    delivery_address = NestedModel(AddressSchema, attribute='delivery_address')
    payment_configuration = NestedModel(PaymentConfiguration, attribute='payment_configuration')
