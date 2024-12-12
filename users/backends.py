from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q as _

UserModel = get_user_model()


class BSSBBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserModel.objects.get(
                _(username__iexact=username) | _(email__iexact=username)
            )
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
            return None
        except UserModel.MultipleObjectsReturned:
            user = UserModel.objects.filter(
                _(username__iexact=username) | _(email__iexact=username)
            ).order_by('id').first()
        else:
            if user.check_password(password):
                return user
        
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
