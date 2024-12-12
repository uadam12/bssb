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
def dashboard(request):
    officials = User.objects.officials()
    applicants = User.objects.applicants()
    
    return render(
        request, 'officials/dashboard', 
        title='BSSB Official Dashboard',
        total_blocked_users = officials.count(),
        total_open_scholarships = Scholarship.objects.count(),
        total_scholarships = Scholarship.objects.count(),
        total_applicants = applicants.count(),
        total_users = applicants.count() + officials.count(),
        total_admins = applicants.count(),
        total_guests = officials.count(),
    )

@officials_only(main_admin_only=not True)
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

@officials_only(main_admin_only=not True)
def create_official(request):
    return create_view(
        request, form_class=OfficialForm,
        success_url='official:admins',
        form_header='Create Admin'
    )

@officials_only()
def delete_official(request, id):
    admin = get_object_or_404(User, id=id, access_code__in=[2,3])

    return delete_view(
        request, model=admin, header='Delete Official'
    )

@officials_only()
def update_official(request, id):
    admin = get_object_or_404(User, id=id)
    
    return update_view(
        request, form_class=OfficialForm,
        instance=admin, 
        form_header='Update Official',
    )

@officials_only()
def applicants(request):
    filter = ApplicantFilter(request.GET, queryset=User.objects.filter(access_code__in=[0,1]))

    return data_view(
        request, data=filter.qs,
        filter_form = filter.form,
        data_template='officials/applicants.html',
        main_template='officials/all-applicants',
        title='Applicants',
    )


def block_applicant(request, applicant_id):
    if not is_post(request) or request.user.access_code < 3:
        return HttpResponse('Invalid request')
    
    user = get_or_none(User, id=applicant_id)
    if user is not None:
        user.access_code = 0
        user.save()

    return render(request, 'parts/applicant-access', applicant=user)

def unblock_applicant(request, applicant_id):
    if not is_post(request) or request.user.access_code < 3:
        return HttpResponse('Invalid request')
    
    user = get_or_none(User, id=applicant_id)
    if user is not None:
        user.access_code = 1
        user.save()

    return render(request, 'parts/applicant-access', applicant=user)