import os
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.lib.payment_providers.razorpay import razorpay


router = APIRouter(prefix="/v1/webhooks/razorpay")


RAZORPAY_WEBHOOK_SECRET = os.environ["RAZORPAY_WEBHOOK_SECRET"]


@router.post("")
async def handle_event(request: Request):
    body = await request.body()
    signature = request.headers.get("X-Razorpay-Signature")
    razorpay.utility.verify_webhook_signature(body, signature, RAZORPAY_WEBHOOK_SECRET)
    return JSONResponse({}, status_code=200)
