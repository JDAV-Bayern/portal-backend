from django.contrib import admin

from import_export import resources, fields, widgets
from import_export.admin import ImportExportModelAdmin

from sections.models import Federation, Section


class FederationForeignKeyWidget(widgets.ForeignKeyWidget):
    model = Federation
    field = "name"

    def __init__(self, level, **kwargs):
        super().__init__(self.model, self.field, **kwargs)
        self.level = level

    def get_queryset(self, value, row, *args, **kwargs):
        return self.model.objects.filter(type=self.level)


class SectionResource(resources.ModelResource):
    number = fields.Field(attribute="number", column_name="Nr")
    name = fields.Field(attribute="name", column_name="Name")
    state = fields.Field(
        attribute="state",
        column_name="Land",
        widget=FederationForeignKeyWidget(level=Federation.STATE),
    )
    district = fields.Field(
        attribute="district",
        column_name="Bezirk",
        widget=FederationForeignKeyWidget(level=Federation.DISTRICT),
    )

    class Meta:
        model = Section


class SectionAdmin(ImportExportModelAdmin):
    resource_class = SectionResource


admin.site.register(Federation)
admin.site.register(Section, SectionAdmin)
