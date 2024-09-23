from django.contrib import admin
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin

from courses.forms import CourseImportForm, CourseConfirmImportForm
from courses.models import Course, CourseYear


class CourseResource(resources.ModelResource):
    number = fields.Field(attribute="number", column_name="KursNr")
    name = fields.Field(attribute="name", column_name="Titel")
    start_date = fields.Field(attribute="start_date", column_name="von")
    end_date = fields.Field(attribute="end_date", column_name="bis")
    location = fields.Field(attribute="location", column_name="Kursort")

    def after_init_instance(self, instance, new, row, **kwargs):
        instance.type = row.get("KursNr")[4:]
        instance.year = kwargs["year"]
        instance.federation = kwargs["federation"]

    class Meta:
        model = Course
        exclude = ["type", "year", "federation"]


class CourseAdmin(ImportExportModelAdmin):
    list_display = ["number", "type", "name", "start_date", "end_date", "location"]

    resource_class = CourseResource
    import_form_class = CourseImportForm
    confirm_form_class = CourseConfirmImportForm

    def get_confirm_form_initial(self, request, import_form):
        initial = super().get_confirm_form_initial(request, import_form)
        if import_form:
            initial["year"] = import_form.cleaned_data["year"].id
            initial["federation"] = import_form.cleaned_data["federation"].id
        return initial
    
    def get_import_data_kwargs(self, request, *args, **kwargs):
        form = kwargs.get("form")
        if form:
            kwargs.update({
                "year": form.cleaned_data["year"],
                "federation": form.cleaned_data["federation"]
            })
        return kwargs


admin.site.register(CourseYear)
admin.site.register(Course, CourseAdmin)
