import re
from django.core.exceptions import ValidationError

def validate_phone_number(phone_number:str) -> str|None:
    pattern = r"^(?:\+234|234|0)(7|8|9)\d{9}$"
    phone_number_match = re.match(pattern, phone_number)
    
    if not phone_number_match:
        raise ValidationError("Invalid phone number!!!")
    
    return phone_number

def validate_bank(bank):
    print(bank)
    
    return bank