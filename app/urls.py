from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('main.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('auths.urls')),
    path('user/', include('users.urls')),
    path('board/', include('board.urls')),
    path('support/', include('support.urls')),
    path('payment/', include('payment.urls')),
    path('academic/', include('academic.urls')),
    path('applicant/', include('applicant.urls')),
    path('officials/', include('users.official_urls')),
    path('scholarships/', include('scholarship.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, 
        document_root=settings.MEDIA_ROOT
    )