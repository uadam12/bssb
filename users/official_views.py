from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from app import render, is_post, get_or_none
from app.views import create_view, delete_view, update_view, data_view
from app.auth import officials_only
from scholarship.models import Scholarship
from .filters import OfficalFilter, ApplicantFilter
from .official_forms import OfficialForm
from .models import User


@officials_only()
def profile(request):
    return render(
        request, 'officials/profile', 
        title='Official Profile',
    )

@officials_only()
def dashboard(request):
    return render(
        request, 'officials/dashboard', 
        title='Official Dashboard',
        total_blocked_users = User.objects.blocks().count(),
        total_open_scholarships = Scholarship.objects.count(),
        total_scholarships = Scholarship.objects.count(),
        total_applicants = User.objects.applicants().count(),
        total_users = User.objects.non_main_admins().count(),
        total_admins = User.objects.admins().count(),
        total_guests = User.objects.guests().count(),
    )

@officials_only(main_admin_only=True)
def officials(request):
    filter = OfficalFilter(
        request.GET, queryset=User.objects.filter(
            access_code__in=[2,3]
        )
    )
    return data_view(
        request, data=filter.qs,
        filter_form = filter.form,
        data_template='officials/index.html',
        title='Officials', add_url=reverse('official:create'),
        table_headers=['S/N', 'Official Name', 'Email Address', 'Type', 'Actions']
    )

@officials_only(main_admin_only=True)
def create_official(request):
    return create_view(
        request, form_class=OfficialForm,
        success_url='official:admins',
        form_header='Create Admin'
    )

@officials_only(main_admin_only=True)
def delete_official(request, id):
    admin = get_object_or_404(User, id=id, access_code__in=[2,3])

    return delete_view(
        request, model=admin, header='Delete Official'
    )

@officials_only(main_admin_only=True)
def update_official(request, id):
    admin = get_object_or_404(User, id=id)
    
    return update_view(
        request, form_class=OfficialForm,
        instance=admin, 
        form_header='Update Official',
    )

@officials_only(admin_only=True)
def applicants(request):
    filter = ApplicantFilter(request.GET, queryset=User.objects.filter(access_code__in=[0,1]))

    return data_view(
        request, data=filter.qs,
        filter_form = filter.form,
        data_template='officials/applicants.html',
        main_template='officials/all-applicants',
        title='Applicants',
    )

@officials_only(admin_only=True)
def block_applicant(request, applicant_id):
    if not is_post(request):
        return HttpResponse('Invalid request')
    
    user:User = get_or_none(User, id=applicant_id)
    if user is not None:
        user.is_blocked = True
        user.save()

    return render(request, 'parts/applicant-access', applicant=user)

@officials_only(admin_only=True)
def unblock_applicant(request, applicant_id):
    if not is_post(request) or request.user.access_code < 3:
        return HttpResponse('Invalid request')
    
    user:User = get_or_none(User, id=applicant_id)
    if user is not None:
        user.is_blocked = False
        user.save()

    return render(request, 'parts/applicant-access', applicant=user)