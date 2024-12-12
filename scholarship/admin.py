from django.contrib import admin
from .models import Scholarship, Application, ApplicationDocument, Document

# Register your models here.
admin.site.register(Scholarship)
admin.site.register(Application)
admin.site.register(ApplicationDocument)
admin.site.register(Document)
