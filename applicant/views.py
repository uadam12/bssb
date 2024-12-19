from django.shortcuts import  get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q
from applicant.models import Referee
from users.forms import ProfilePictureForm
from app import is_post, get_or_none, render, render_form
from app.views import create_view, update_view, delete_view
from app.auth import applicant_only, complete_profile_required
from scholarship.models import Scholarship, Application
from .forms import (
    PersonalInformationForm, PersonalInformation,
    AcademicInformationForm, AcademicInformation,
    AccountBankForm, AccountBank, RefereeForm,
    SchoolAttendedForm, SchoolAttended,
    DocumentForms, ApplictionDocumentForm
)


# Create your views here.
@applicant_only
def dashboard(request):
    applications = Application.objects.filter(
        Q(applicant=request.user) &
        ~Q(status='incomplete')
    )
    return render(
        request, 'applicants/dashboard', 
        applications = applications,
        title = 'My Dashboard', 
    )

@applicant_only
def change_profile_picture(request):
    if is_post(request):
        form = ProfilePictureForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid() and form.save():
            messages.success(request, 'Profile picture updated successfully!!!')
            return render(request, 'parts/profile-img')

    messages.error(request, 'Invalid request')
    return HttpResponse(status=400)

@applicant_only
def profile(request):
    user = request.user
    applicant = get_or_none(PersonalInformation, user=user)
    academic_info = get_or_none(AcademicInformation, user=user)
    account_bank = get_or_none(AccountBank, user=user)
    referee = get_or_none(Referee, user=user)
    documents = user.registration_documents

    return render(
        request, 'applicants/profile', 
        title='Applicant Profile',
        applicant_form = PersonalInformationForm(instance=applicant),
        academic_form = AcademicInformationForm(instance=academic_info),
        profile_picture_form = ProfilePictureForm(instance=request.user),
        bank_form = AccountBankForm(instance=account_bank),
        referee_form = RefereeForm(instance=referee),
        schools = SchoolAttended.objects.filter(user=request.user),
        document_forms = DocumentForms(queryset=documents),
        data_url = reverse_lazy('applicant:schools-attended'),
        documents = documents, with_htmx = True, with_modal = True,
        data_template="applicants/schools.html",  data_header='Schools Attended',
        add_url=reverse_lazy('applicant:add-school'), table_headers = [
            'School Name', 'Certificate Obtained', 'Year Started', 'Year Finish', 'Actions'
        ]
    )

@applicant_only
def personal_information(request):
    form = PersonalInformation()

    if is_post(request):
        info = get_or_none(PersonalInformation, user=request.user)
        form = PersonalInformationForm(request.POST, instance=info)

        if form.is_valid():
            info = form.save(False)
            info.user = request.user
            info.save()

            messages.success(request, 'Personal Information save successfully.')
    return render_form(request, form)


@applicant_only
def academic_information(request):
    form = AcademicInformationForm()

    if is_post(request):
        info = get_or_none(AcademicInformation, user=request.user)
        form = AcademicInformationForm(request.POST, instance=info)

        if form.is_valid():
            info = form.save(False)
            info.user = request.user
            info.save()
            
            messages.success(request, "Academic Information Save successfully.")
    return render_form(request, form)

@applicant_only
def account_details(request):
    form = AccountBankForm()

    if is_post(request):
        account_bank = get_or_none(AccountBank, user=request.user)
        form = AccountBankForm(request.POST, instance=account_bank)

        if form.is_valid():
            account_bank:AccountBank = form.save(False)
            account_bank.user = request.user
            account_bank.save()
            messages.success(request, "Account bank details Save successfully.")
            
    return render_form(request, form)

@applicant_only
def schools_attended(request):
    schools = SchoolAttended.objects.filter(user=request.user).all()
    return render(request, 'applicants/schools', schools=schools)

@applicant_only
def add_school(request):
    def save(school):
        school.user = request.user
        school.save()
        messages.success(request, f"{school} added.")

    return create_view(
        request, SchoolAttendedForm,
        'applicant:profile', 'Add School',
        save_instantly=False,
        further_action = save
    )

@applicant_only
def update_school(request, pk):
    school = get_object_or_404(SchoolAttended, pk=pk)

    def save(school):
        messages.success(request, f"{school} updated.")
    
    return update_view(
        request, SchoolAttendedForm, school,
        'applicant:schools-attended',
        form_header='Update School',
        further_action = save
    )

@applicant_only
def delete_school(request, pk):
    school = get_object_or_404(SchoolAttended, pk=pk)
    return delete_view(request, school, 'applicant:profile', 'Delete School')

@applicant_only
def documents(request):
    docs = request.user.registration_documents
    form = DocumentForms(queryset=docs)

    if is_post(request):
        form = DocumentForms(data=request.POST, files=request.FILES, queryset=docs)
        if form.is_valid() and form.save():
            messages.success(request, "Registration documents uploaded successfully!!!")

        return render(
            request, 'parts/applicant-documents', document_forms = form,
            documents = docs
        )
    
    return render_form(request, form)

@applicant_only
def referees(request):
    form = RefereeForm()

    if is_post(request):
        referee = get_or_none(Referee, user=request.user)
        form = RefereeForm(request.POST, instance=referee)
        
        if form.is_valid(): 
            referee = form.save(False)
            referee.user = request.user
            referee.save()
            messages.success(request, "Referee Save successfully.")    

    return render_form(request, form)

@complete_profile_required
def scholarships(request):
    field_of_study = request.user.academic_info.field_of_study
    scholarships = Scholarship.objects.filter(
        field_of_studies=field_of_study, 
        application_commence__lt=timezone.now(),
        application_deadline__gt=timezone.now(),
    ).exclude(
        Q(application__applicant=request.user)
        & ~Q(application__status='incomplete')
    ).distinct()
    
    return render(
        request, 'applicants/scholarships', 
        scholarships = scholarships,
        title="Open Scholarships"
    )

@complete_profile_required
def apply(request, id):
    scholarship = get_object_or_404(Scholarship, id=id)
    application = Application.objects.filter(scholarship=scholarship, applicant=request.user).first()

    if not (application and application.application_fee_payment):
        return redirect('payment:application-fee', id=id)
    
    if application.status != 'incomplete':
        messages.info(application, 'Application completed already.')
        return redirect('applicant:dashboard')
    
    app_docs = application.get_documents
    form = ApplictionDocumentForm(queryset=app_docs)
    form.is_valid()

    if is_post(request):
        form = ApplictionDocumentForm(
            data=request.POST, files=request.FILES, queryset=app_docs
        )
        if form.is_valid():
            form.save()
            messages.success(request, f'You have successfully applied for {scholarship}')
            application.status = 'pending'
            application.save()
            return redirect('applicant:dashboard')

    return render(
        request, 'applicants/apply', 
        title=f"Application for {scholarship}",
        scholarship = scholarship, forms = form,
    )