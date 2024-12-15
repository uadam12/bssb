from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class BSSBManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('Email address is required.'))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)
    
    def blocks(self):
        return self.get_queryset().filter(is_blocked=True)
    
    def applicants(self):
        return self.get_queryset().filter(access_code=1)
    
    def non_main_admins(self):
        return self.get_queryset().filter(access_code__lt=4)
    
    def guests(self):
        return self.get_queryset().filter(access_code=2)
    
    def admins(self):
        return self.get_queryset().filter(access_code=3)