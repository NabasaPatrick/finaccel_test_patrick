from fastapi import APIRouter
from .user.api import router as user_router
from .master_limit.api import router as limit_router
from .user_limit.api import router as usr_limit_router
from .loan.api import router as loan_router
from .payment.api import router as payment_router

router = APIRouter(prefix='/api')

router.include_router(user_router)
router.include_router(limit_router)
router.include_router(usr_limit_router)
router.include_router(loan_router)
router.include_router(payment_router)
