from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from app import render, is_post, get_or_none
from app.auth import login_required, officials_only
from app.pdf import generate_application_form
from app.views import data_view
from .models import Scholarship, Application
from .filters import ApplicationFilter

@officials_only()
def applications(request):
    scholarships = Scholarship.objects.all()
    
    return render(
        request, 'application/index',
        title='Scholarship Applications',
        scholarships = scholarships
    )
    
@officials_only()
def scholarship_applications(request, id):
    scholarship = get_object_or_404(Scholarship, id=id)
    applications = scholarship.applications.all()
    filter = ApplicationFilter(request.GET, queryset=applications)

    return data_view(
        request, filter.qs,
        data_template='scholarship/applications.html',
        table_headers=['S/N', 'Applicant name', 'Bank details', 'Action'],
        title=f"{scholarship} Applications",
        filter_form=filter.form
    )


@officials_only()
def scholarship_disbursements(request, id):
    scholarship = get_object_or_404(Scholarship, id=id)
    filter = ApplicationFilter(
        request.GET, 
        queryset=scholarship.applications.all()
    )
    
    return data_view(
        request, filter.qs,
        data_template='scholarship/disbursements.html',
        table_headers=['S/N', 'Applicant name', 'Bank details', 'Action'],
        title=f"{scholarship} Disbursements",
        filter_form=filter.form
    )

def approve_application(request, id):
    if not is_post(request) or request.user.access_code < 3:
        return HttpResponse('Invalid request')
    
    application:Application = get_or_none(Application, id=id)
    
    if application is not None:
        application.status = 'approved'
        application.save()

    return render(request, 'parts/application-status', application=application)

def reject_application(request, id):
    if not is_post(request) or request.user.access_code < 3:
        return HttpResponse('Invalid request')
    
    application:Application = get_or_none(Application, id=id)
    
    if application is not None:
        application.status = 'rejected'
        application.save()

    return render(request, 'parts/application-status', application=application)


@login_required
def application(_, application_id):
    application = get_object_or_404(Application, application_id=application_id)
    application_form = generate_application_form(application)
    response = HttpResponse(content_type='application/pdf')
    filename = f"{application.application_id} Application Form.pdf"
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    response.write(application_form)
    
    return response