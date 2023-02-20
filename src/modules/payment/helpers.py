import datetime

from dateutil.relativedelta import relativedelta
from fastapi import HTTPException
from fastapi_sqlalchemy import db
from sqlalchemy.sql import or_

from src.modules.loan.model import Loan
from src.modules.master_limit.model import MLimit
from src.modules.payment.model import Payment
from src.modules.payment.schema import PaymentSchemaIn, PaymentSchema, PaymentSchemaUpdateIn
from src.modules.user_limit.model import UserLimit


def get_payment_by_id(id):
    payment = db.session.get(Payment, id)
    if not payment:
        raise HTTPException(404, 'Payment Not found')
    return payment


def get_payment_query(user_id):
    filters = []
    if id:
        filters.append(Payment.user_id == user_id)
    query = db.session.query(Payment).filter(*filters)
    return query


def get_payment_count(user_id):
    query = get_payment_query(user_id)
    return query.count()


def get_payments(user_id=None):
    query = get_payment_query(user_id)
    return query.all()


def add_payment(data: PaymentSchemaIn) -> PaymentSchema:
    loan: Loan = Loan.get(data.loan_id)
    today = datetime.date.today()
    if loan and loan.status == 'active':
        limit: UserLimit = UserLimit.get(loan.user_limit)
        loan.total_paid += data.amount
        loan.last_payment_date = today
        loan.next_payment_date = loan.next_payment_date + relativedelta(months=+1)
        if limit:
            limit.outstanding_balance -= data.amount
            limit.limit_balance += data.amount
        else:
            raise HTTPException(404, 'User Limit Not found')
    else:
        raise HTTPException(404, 'Loan Not found')

    payment = Payment(
        **data.dict()
    )
    db.session.add(payment)
    db.session.commit()

    return PaymentSchema.from_orm(payment)
