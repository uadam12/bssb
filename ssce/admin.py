from django.contrib import admin
from .models import SSCE, Subject, Grade, Record

# Register your models here.
admin.site.register(SSCE)
admin.site.register(Subject)
admin.site.register(Grade)
admin.site.register(Record)