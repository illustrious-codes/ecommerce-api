import random
import re
import string

from django.dispatch import receiver
from notifications.email import Email

def message(subject: str, extra: str) -> str:
    if subject.lower() == "email verification":
        message = f"Your email verification is {extra}"
        email_template = "email/email_verification.html"
    else: 
        email_template = ""
        message = ""
    return message, email_template

def generate_otp(user: object) -> str:
    otp = "".join(random.choices(string.digits, k=6))
    return otp

def send_otp(user: object, email: str, subject: str) -> bool:
    otp = generate_otp(user)
    extra = {"otp_code": otp}
    send_email(email, subject, extra)

def send_email(email: str, subject: str, extra: dict = None):
    message_, template_ = message(subject, extra)
    data = extra if extra else {}
    # if extra: 
    #     data = extra

    Email(
        subject=subject,
        receiver=email,
        plain_message=f"{message_}",
        template=template_,
        data=data
    ).send()
    return True