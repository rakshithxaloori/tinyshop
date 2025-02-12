import random
import string


def generate_secret_key(livemode: bool):
    prefix = "sk_live_" if livemode else "sk_test_"
    random_string = "".join(random.choices(string.ascii_letters + string.digits, k=24))
    return f"{prefix}{random_string}"
