from itsdangerous import URLSafeTimedSerializer
from django.conf import settings

serializer = URLSafeTimedSerializer(settings.SECRET_KEY)

def generate_token(email:str) -> str:
    return serializer.dumps(email)

def verify_token(token) -> str | None:
    try:
        email = serializer.loads(token, max_age=600)
        return email
    except Exception:
        return None