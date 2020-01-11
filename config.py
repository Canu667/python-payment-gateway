import os


class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev-database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BILLPAY_MERCHANT_ID = os.environ['BILLPAY_MERCHANT_ID']
    BILLPAY_PRIVATE_PORTAL_ID = os.environ['BILLPAY_PRIVATE_PORTAL_ID']
    BILLPAY_PRIVATE_PASSWORD_HASH = password_hash = os.environ['BILLPAY_PRIVATE_PASSWORD_HASH']
    BILLPAY_BUSINESS_PORTAL_ID = os.environ['BILLPAY_BUSINESS_PORTAL_ID']
    BILLPAY_BUSINESS_PASSWORD_HASH = os.environ['BILLPAY_BUSINESS_PASSWORD_HASH']
    BILLPAY_API_URL = os.environ['BILLPAY_API_URL']
