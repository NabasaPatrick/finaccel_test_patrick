from fastapi import APIRouter, Query

from src.modules.loan.helpers import get_loans, get_loan_count, add_loan, info_loan
from src.modules.loan.model import Loan
from src.modules.loan.schema import LoanListResponse, LoanResponse, LoanSchemaIn, LoanInfoResponse

router = APIRouter(prefix='/loan', tags=['Loan'])


@router.get("", response_model=LoanListResponse)
def get_loan(search: str = Query(None)):
    loans = get_loans(search)
    count = get_loan_count(search)
    return LoanListResponse.parse_obj({
            'result': loans,
            'meta': {
                'count': count
            }
        })


@router.post("", response_model=LoanResponse)
def post_loan(data: LoanSchemaIn):
    loan = add_loan(data)
    return LoanResponse(result=loan)


@router.get("/info", response_model=LoanInfoResponse)
def info_loan(loan_id: str):
    loan = Loan.get(loan_id)
    info = info_loan(loan)
    return LoanInfoResponse(result=info)
