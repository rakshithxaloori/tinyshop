import os
import razorpay as razorpay_lib


razorpay = razorpay_lib.Client(
    auth=(os.environ["RAZORPAY_KEY_ID"], os.environ["RAZORPAY_KEY_SECRET"])
)
