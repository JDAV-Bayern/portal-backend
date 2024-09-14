from django import forms
from django.utils.translation import gettext_lazy as _
from import_export.forms import ImportForm, ConfirmImportForm

from courses.models import CourseYear
from sections.models import Federation


class CourseFormMixin(forms.Form):
    year = forms.ModelChoiceField(queryset=CourseYear.objects.all(), required=True, label=_("Course Year"))
    federation = forms.ModelChoiceField(
        queryset=Federation.objects.all(), required=True, label=_("Federation")
    )


class CourseImportForm(CourseFormMixin, ImportForm):
    pass


class CourseConfirmImportForm(CourseFormMixin, ConfirmImportForm):
    pass
