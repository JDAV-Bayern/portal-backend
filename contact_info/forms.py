from django import forms
from django.utils.translation import gettext_lazy as _
from import_export.forms import ImportForm, ConfirmImportForm

from contact_info.models import Country


class LocalityFormMixin(forms.Form):
    country = forms.ModelChoiceField(queryset=Country.objects.all(), required=True, label=_("Country"))


class LocalityImportForm(LocalityFormMixin, ImportForm):
    pass


class LocalityConfirmImportForm(LocalityFormMixin, ConfirmImportForm):
    pass
