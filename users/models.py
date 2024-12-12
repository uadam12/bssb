import os
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.templatetags.static import static
from django.contrib.auth.models import AbstractUser
from app import compress
from board.models import RegistrationDocument
from payment.models import Payment
from .managers import BSSBManager, _


# Create your models here.
class User(AbstractUser):
    ACCESS_CODES = (
        (1, 'Applicant'),
        (2, 'Guest User'),
        (3, 'Administrator'),
        (4, 'Main Admin')
    )
    username = None
    email = models.EmailField(_('email address'), unique=True)
    access_code = models.PositiveSmallIntegerField(default=1, choices=ACCESS_CODES)
    is_blocked = models.BooleanField(default=False)
    has_completed_profile = models.BooleanField(default=False)
    paid_registration_fee = models.BooleanField(default=False)
    picture = models.ImageField(default='/static/default-user.svg', upload_to='profiles')
    last_time_read_notifications = models.DateTimeField(default=timezone.now, blank=True)
    registration_fee_payment = models.OneToOneField(Payment, default=None, null=True, on_delete=models.SET_DEFAULT, related_name='applicant')
    otp_enabled = models.BooleanField(default=False)

    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = BSSBManager()
    
    @property
    def avatar(self):
        file = os.path.join(settings.MEDIA_ROOT, self.picture.name)
        if self.picture and os.path.isfile(file):
            return self.picture.url
        
        return static('imgs/default-user.svg')
    
    @property
    def registration_documents(self):
        reg_docs = RegistrationDocument.objects.all()
        
        for reg_doc in reg_docs:
            Document.objects.get_or_create(owner=self, reg=reg_doc)
            
        
        return Document.objects.filter(owner=self)

    @property
    def profile_error_messages(self) -> list:
        profile_errors = []
        error_messages = {
            'personal_info': 'Please update your personal information.',
            'academic_info': 'Please add your current academic information.',
            'account_bank': 'Please add your account bank details.',
            'schools_attended': 'Please add school(s) you attended before.',
            'referee': 'Please provide us with your referee details.'
        }
        
        if self.picture.url.endswith('.svg'):
            profile_errors.append('Please update your profile picture.')
        
        for field, message in error_messages.items():
            if not hasattr(self, field):
                profile_errors.append(message)
                
        return profile_errors

    @property
    def dashboard(self):
        viewname = 'applicant:dashboard' if self.access_code < 2 else 'official:dashboard'
        return reverse(viewname)
    
    @property
    def profile(self):
        viewname = 'applicant:profile' if self.access_code < 2 else 'official:profile'
        return reverse(viewname)
    
    def save(self, *args, **kwargs):
        try:
            self.picture = compress(self.picture)
        except: pass
        
        super().save(*args, **kwargs)

    def __str__(self):
        name = f"{self.first_name} {self.last_name}"
        name = name.strip()
        
        return name if name else self.email


class Document(models.Model):
    image = models.ImageField(upload_to='registration_documents', null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    reg = models.ForeignKey(RegistrationDocument, on_delete=models.CASCADE, related_name='documents')
    
    def save(self, *args, **kwargs):
        try:
            self.picture = compress(self.image)
        except: pass
        
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.reg.name} of {self.owner}"