from extensions import db
from enum import Enum


class PaymentStatus(Enum):
    RESERVED = 'reserved'
    CAPTURED = 'captured'
    FINISHED = 'finished'


class PaymentModel(db.Model):
    __tablename__ = 'payment'

    id = db.Column(db.Integer, primary_key=True)
    payment_method = db.Column(db.String(100), nullable=False)
    reference_id = db.Column(db.String(100), nullable=False)
    transaction_id = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum(PaymentStatus), nullable=False)

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()
