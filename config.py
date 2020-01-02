import os


class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev-database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BILLPAY_API_MERCHANT_ID = 4549
    BILLPAY_API_PORTAL_ID_PRIVATE = 8305
    BILLPAY_API_SECURITY_CODE_PRIVATE = 'zGl7HvD52YwN'
    BILLPAY_API_URL = 'https://test-api.billpay.de/v2/xml/offline'