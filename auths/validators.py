import re
from django.core.exceptions import ValidationError
from applicant.models import PersonalInformation
from payment.remita import remita

data = {}


def validate_nin(nin):
        nin_format = r'\d{11}'
        nin_match = re.match(nin_format, nin)
        
        if not nin_match:
            raise ValidationError("Invalid NIN")

        info = PersonalInformation.objects.filter(nin=nin)
        if info.exists():
            raise ValidationError(f"Applicant with this National Identification Number(NIN: {nin}) already exists.")

        if nin not in data:
            data[nin] = remita.get_nin_data(nin)
        
        nin_data = data.get(nin)
        
        if nin_data.get('stateOfOriginCode') != 'BO':
            raise ValidationError('This program is only applicable to Borno state indigen.')

        
        return nin