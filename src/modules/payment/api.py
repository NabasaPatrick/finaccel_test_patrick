from fastapi import APIRouter, Query

from src.modules.payment.helpers import get_payments, get_payment_count, add_payment
from src.modules.payment.schema import PaymentListResponse, PaymentResponse, PaymentSchemaIn

router = APIRouter(prefix='/payment', tags=['Payment'])


@router.get("", response_model=PaymentListResponse)
def get_payment(user_id: str):
    payments = get_payments(user_id)
    count = get_payment_count(user_id)
    return PaymentListResponse.parse_obj({
            'result': payments,
            'meta': {
                'count': count
            }
        })


@router.post("", response_model=PaymentResponse)
def post_payment(data: PaymentSchemaIn):
    payment = add_payment(data)
    return PaymentResponse(result=payment)
