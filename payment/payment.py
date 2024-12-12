import requests

class PaymentAPI:
    def __init__(self):
        self.key = "sk_test_ad19c74552082f0d0e963480de5f0cef5cd3f5eb"

    def get_headers(self, json_type=False, headers: dict = {}):
        headers.update({
            "Authorization": f"Bearer {self.key}",
            **headers
        })

        if json_type: headers.update({
            "Content-Type": "application/json"
        })

        return headers

    def url(self, amount, user, redirect_url):
        url = 'https://api.paystack.co/transaction/initialize'
        headers = self.get_headers(
            json_type=True
        )
        
        body = {
            'email': user.email,
            'amount': amount * 100,
            'callback_url': redirect_url
        }
        
        res = requests.post(
            url = url,
            headers = headers,
            json = body
        )
        data = res.json().get('data', {})
        url = data.get('authorization_url', '')
        return url

    def verify(self, ref, amount):
        url = f"https://api.paystack.co/transaction/verify/{ref}"
        headers = self.get_headers()

        res = requests.get(url, headers=headers).json()
        data = res.get('data', {})
        
        if data.get('status') != 'success':
            return False
        
        return int(data.get('amount', '0')) >= amount

        
payment = PaymentAPI()

