from time import sleep

from django.contrib.auth import get_user_model
import string
from random import choice


User = get_user_model()


def create_invite_code():
    existing_codes = User.objects.values_list("invite_code", flat=True)
    alphabet = string.ascii_letters + string.digits
    while True:
        code = ""
        for _ in range(6):
            code += choice(alphabet)
        if code not in existing_codes:
            break
    return code


def create_one_time_code():
    code = ""
    for _ in range(4):
        code += choice(string.digits)
    return code


def send_code(phone, code):
    print(f"phone: {phone} | code: {code}")
    sleep(2)
