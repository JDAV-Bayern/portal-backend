from django.contrib import admin

from reimbursements.models import CourseDetails, TravelDetails, Reimbursement


class CourseDetailsInline(admin.StackedInline):
    model = CourseDetails
    extra = 0


class TravelDetailsInline(admin.StackedInline):
    model = TravelDetails
    extra = 0


class ReimbursementAdmin(admin.ModelAdmin):
    inlines = [CourseDetailsInline, TravelDetailsInline]


admin.site.register(Reimbursement, ReimbursementAdmin)
