from django.forms import Form
from django_filters import FilterSet
from crispy_forms.layout import HTML
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FieldWithButtons

    
class FilterDataSet(FilterSet):
    @property
    def form(self) -> Form:
        form = super().form

        form.helper = FormHelper()
        form.helper.form_tag = False
        form.helper.disable_csrf = True

        return form

    def search_field_with_btn(self, field:str) -> FieldWithButtons:
        return FieldWithButtons(field, HTML("""
            <button class='btn btn-secondary'>
                <i class='bi bi-search'></i>
            </button>
            """
        ))