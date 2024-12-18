import requests, hashlib, random, json
from django.conf import settings
from users.models import User


class Remita:
    def __init__(self):
        self.base_url = settings.BASE_URL
        self.serviceTypeId = settings.SERVICE_TYPE_ID
        self.merchantId = settings.MERCHANT_ID
        self.apiKey = settings.API_KEY

    def sha512(self, inputString):
        hashed_input = hashlib.sha512(inputString.encode('utf-8'))
        return hashed_input.hexdigest()

    def init_payment(self, totalAmount, user:User, description:str=''):
        orderId = str(random.random() * 1000000000)
        apiHash = self.sha512(f"{self.merchantId}{self.serviceTypeId}{orderId}{totalAmount}{self.apiKey}")
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"remitaConsumerKey={self.merchantId},remitaConsumerToken={apiHash}"
        }
        payload = {
            'serviceTypeId': self.serviceTypeId,
            'amount': str(totalAmount),
            'orderId': orderId,
            'payerName': str(user),
            'payerEmail': user.email,
            'payerPhone': user.personal_info.phone_number,
            'description': description
        }
        response = requests.post(
            f"{self.base_url}echannelsvc/merchant/api/paymentinit", 
            headers=headers, json=payload
        )

        result = response.text
        if result.startswith(('{', '[')):
            return response.json()
        
        a = result.find('(') + 1
        b = result.rfind(')')
        return json.loads(result[a:b])

    def verify_payment(self, rrr):
        apiHash = self.sha512(f"{rrr}{self.apiKey}{self.merchantId}")
        response = requests.get(f"{self.base_url}echannelsvc/{self.merchantId}/{rrr}/{apiHash}/status.reg")
        return response.json()

remita = Remita()