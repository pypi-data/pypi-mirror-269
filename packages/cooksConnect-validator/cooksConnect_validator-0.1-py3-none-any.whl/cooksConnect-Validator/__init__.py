# __init__.py
import re

def validate_email_format(email):
    if '@' not in email:
        raise ValueError("Invalid email format")

def validate_phone_number(contact):
    pattern = re.compile(r'^\+?[\d\- ]+$')
    if not pattern.match(contact):
        raise ValueError("Invalid phone number format")