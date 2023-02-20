import datetime
import pytz
from dateutil.relativedelta import relativedelta

from fastapi import HTTPException
from fastapi_sqlalchemy import db
from sqlalchemy.sql import or_

from src.modules.loan.model import Loan
from src.modules.loan.schema import LoanSchemaIn, LoanSchema, LoanInfoSchema
from src.modules.master_limit.model import MLimit
from src.modules.master_limit.schema import DurationType
from src.modules.user_limit.model import UserLimit


def get_loan_by_id(id):
    loan = db.session.get(Loan, id)
    if not loan:
        raise HTTPException(404, 'Loan Not found')
    return loan


def get_loan_query(search=None):
    filters = []
    if search:
        filters.append(
            or_(
                Loan.status.ilike(f'%{search}%'),
            ))
    query = db.session.query(Loan).filter(*filters)
    return query


def get_loan_count(search=None):
    query = get_loan_query(search)
    return query.count()


def get_loans(search=None):
    query = get_loan_query(search)
    return query.all()


def add_loan(data: LoanSchemaIn) -> LoanSchema:
    ulimit: UserLimit = UserLimit.get(data.user_limit)
    status ='active'
    if ulimit.limit_total > data.total_loan and ulimit.limit_balance > data.total_loan:
        if ulimit.limit_balance > ulimit.limit_total:
            overpaid = ulimit.limit_balance - ulimit.limit_total
            total_loan = data.total_loan - overpaid

            if total_loan < 0:
                ulimit.limit_balance -= data.total_loan
                data.total_loan = 0
                status = 'paid'
            else:
                ulimit.outstanding_balance += total_loan
                ulimit.limit_balance -= data.total_loan
                data.total_loan = total_loan
        else:
            ulimit.outstanding_balance += data.total_loan
            ulimit.limit_balance -= data.total_loan

        mlimit: MLimit = MLimit.get(ulimit.limit_id)
        duration = int(mlimit.limit_duration)
        dur_type = mlimit.duration_type
        if dur_type == DurationType.Day:
            end_date = datetime.datetime.now() + datetime.timedelta(duration)
            tenur = duration/30
        else:
            end_date = datetime.datetime.now() + relativedelta(months=+duration)
            tenur = duration
        next_date = datetime.datetime.now() + relativedelta(months=+1)
        loan = Loan(
            **data.dict(),
            start_date=datetime.datetime.now(),
            est_end_date=end_date,
            loan_tenur=tenur,
            next_payment_date=next_date,
            emi_amt=data.total_loan/tenur,
            status=status,
        )
        db.session.add(loan)
        db.session.commit()
    else:
        raise HTTPException(400, 'Not enough limit')

    return LoanSchema.from_orm(loan)


def info_loan(loan: Loan) -> LoanInfoSchema:
    today = datetime.datetime.now(pytz.timezone("Asia/jakarta"))
    if loan.next_payment_date.date() >= today.date():
        bill_active = loan.last_payment_date < loan.next_payment_date - relativedelta(months=1)
        if bill_active:
            status = "Tagihan bulan ini belum dibayar"
        else:
            status = "Tagihan bulan ini sudah dibayar"
    else:
        late = today.date() - loan.next_payment_date.date()
        status = f"Pinjaman ini mengalami tunggakan {late.days} hari"
    return LoanInfoSchema(
        id=loan.id,
        user_limit=loan.user_limit,
        status=status,
        next_payment_date=loan.next_payment_date,
        is_late=today > loan.next_payment_date,
        total_loan=loan.total_loan,
        bill=loan.emi_amt
    )
