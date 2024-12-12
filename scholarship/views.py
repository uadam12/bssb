from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from app import render, is_post
from app.views import delete_view, create_view, update_view, data_view
from app.auth import officials_only
from academic.models import Program
from .models import ApplicationDocument
from .forms import ScholarshipForm, Scholarship, ApplicationDocumentForm
from .filters import FilterScholarship


# Create your views here.
@officials_only()
def index(request):
    filter = FilterScholarship(request.GET, queryset=Scholarship.objects.all())

    return data_view(
        request=request, 
        title='Scholarships',
        add_url=reverse('scholarship:create'),
        data_template='scholarship/index.html', 
        data = filter.qs, filter_form=filter.form,
        table_headers=[
            'S/N', "Name", 'Application Commence', 
            'Application Deadline', 'Actions'
        ]
    )

@officials_only()
def scholarship(request, id):
    scholarship:Scholarship = get_object_or_404(
        Scholarship.objects.prefetch_related('field_of_studies'), id=id
    )
    
    return render(
        request, 'scholarship/info',
        with_htmx=True, with_modal=True,
        data_template='board/reg-documents.html',
        scholarship = scholarship, title=f"{scholarship} details",
        table_headers=['S/N', 'Name', 'Is Compulsory', 'Actions'],
        data_url=reverse('scholarship:app-documents', kwargs={'id': id}),
        data=ApplicationDocument.objects.filter(scholarship=scholarship).all(),
        add_url=reverse('scholarship:create-app-document', kwargs={'id': id}),
    )

# Application Documents
def app_docuements(request, id):
    return data_view(
        request, data_template='board/reg-documents.html',
        table_headers=['S/N', 'Name', 'Is Compulsory', 'Actions'],
        data=ApplicationDocument.objects.filter(scholarship_id=id).all(),
        add_url=reverse('scholarship:create-app-document', kwargs={'id': id}),
        title='Application Documents'
    )

def create_app_docuement(request, id):
    scholarship = get_object_or_404(Scholarship, id=id)
    
    def save(app_doc:ApplicationDocument):
        app_doc.scholarship = scholarship
        app_doc.save()
    
    return create_view(
        request, form_class=ApplicationDocumentForm, 
        save_instantly=False, further_action=save,
        success_url='scholarship:app-documents', 
        form_header='Create Application Document',
    )

def update_app_document(request, id):
    app_doc = get_object_or_404(ApplicationDocument, id=id)
    
    return update_view(
        request, ApplicationDocumentForm, 
        app_doc, "Update Application Document", 
        save_instantly=True
    )

def delete_app_document(request, id):
    app_doc = get_object_or_404(ApplicationDocument, id=id)
    
    return delete_view(
        request, app_doc, "Delete Application Document"
    )

# Scholarship
@officials_only(main_admin_only=True)
def create_scholarship(request):
    return create_view(
        request, 
        form_header='Create Scholarship',
        form_class=ScholarshipForm, 
        success_url='scholarship:index'
    )


@officials_only(main_admin_only=True)
def update_scholarship(request, id):
    scholarship = get_object_or_404(Scholarship, id=id)
    
    return update_view(
        request, 
        instance=scholarship,
        form_header=f'Update {scholarship}',
        form_class=ScholarshipForm
    )
    
@officials_only(main_admin_only=True)
def delete_scholarship(request, id):
    scholarship = get_object_or_404(Scholarship, id=id)
    
    return delete_view(
        request, 
        model=scholarship,
        header=f'BSSB Delete {scholarship}'
    )


@officials_only(main_admin_only=True)
def field_of_studies(request, id):
    scholarship = get_object_or_404(Scholarship, id=id)
    programs = Program.objects.filter(field_of_studies__isnull=False).distinct()
    
    if is_post(request):
        selected_field_of_studies = request.POST.getlist('field_of_studies', [])
        scholarship.field_of_studies.set(selected_field_of_studies)
        scholarship.save()
        messages.success(request, 'Field of studies updated successfully.')
        return redirect(scholarship.url)
    
    return render(
        request, 'scholarship/field-of-studies', scholarship=scholarship,
        title=f"Manage field of studies of {scholarship}",
        programs=programs
    )