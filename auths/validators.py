import re
from django.core.exceptions import ValidationError
from applicant.models import PersonalInformation
from app.validators import validate_phone_number


def validate_phone(phone_number):
    phone_number = validate_phone_number(phone_number)

    if PersonalInformation.objects.filter(phone_number=phone_number).exists():
        raise ValidationError(f"Applicant with this phone number already exists.")
    
    return phone_number

def validate_nin(nin):
    nin_format = r'\d{11}'
    nin_match = re.match(nin_format, nin)
        
    if not nin_match:
        raise ValidationError("Invalid National Identification Number(NIN)")

    if PersonalInformation.objects.filter(nin=nin).exists():
        raise ValidationError(f"Applicant with this National Identification Number(NIN) already exists.")
        
    return nin

def validate_bvn(bvn):
    bvn_format = r'\d{11}'
    bvn_match = re.match(bvn_format, bvn)

    if not bvn_match:
        raise ValidationError("Invalid Bank Verification Number(BVN).")

    if PersonalInformation.objects.filter(bvn=bvn).exists():
        raise ValidationError(f"Applicant with this Bank Verification Number(BVN) already exists.")

    return bvn