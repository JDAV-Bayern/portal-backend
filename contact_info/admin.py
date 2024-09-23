from django.contrib import admin

from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin

from contact_info.forms import LocalityConfirmImportForm, LocalityImportForm
from contact_info.models import Country, Locality


class LocalityResource(resources.ModelResource):
    postal_code = fields.Field(attribute="postal_code", column_name="plz")
    name = fields.Field(attribute="name", column_name="ort")

    def after_init_instance(self, instance, new, row, **kwargs):
        instance.country = kwargs["country"]
        instance.is_admin_provided = True

    class Meta:
        model = Locality
        exclude = ["country", "is_admin_provided"]


class LocalityAdmin(ImportExportModelAdmin):
    list_display = ["postal_code", "name", "country", "is_admin_provided"]

    resource_class = LocalityResource
    import_form_class = LocalityImportForm
    confirm_form_class = LocalityConfirmImportForm

    def get_confirm_form_initial(self, request, import_form):
        initial = super().get_confirm_form_initial(request, import_form)
        if import_form:
            initial["country"] = import_form.cleaned_data["country"].id
        return initial
    
    def get_import_data_kwargs(self, request, *args, **kwargs):
        form = kwargs.get("form")
        if form:
            kwargs.update({
                "country": form.cleaned_data["country"],
            })
        return kwargs


admin.site.register(Country)
admin.site.register(Locality, LocalityAdmin)
