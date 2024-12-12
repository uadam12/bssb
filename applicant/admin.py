from django.contrib import admin
from .models import PersonalInformation, AcademicInformation, AccountBank, Referee

# Register your models here.
admin.site.register(PersonalInformation)
admin.site.register(AcademicInformation)
admin.site.register(AccountBank)
admin.site.register(Referee)
