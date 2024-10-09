from django.contrib import admin

from reimbursements.models import FoodExpense, GenericExpense, TransportExpense, CourseDetails, TravelDetails, Reimbursement, Ticket, CarTrip, Passenger


class CourseDetailsInline(admin.StackedInline):
    model = CourseDetails
    extra = 0


class TravelDetailsInline(admin.StackedInline):
    model = TravelDetails
    extra = 0


class TransportExpenseInline(admin.TabularInline):
    model = TransportExpense
    extra = 0
    show_change_link = True


class FoodExpenseInline(admin.TabularInline):
    model = FoodExpense
    extra = 0


class GenericExpenseInline(admin.TabularInline):
    model = GenericExpense
    extra = 0


class ReimbursementAdmin(admin.ModelAdmin):
    inlines = [CourseDetailsInline, TravelDetailsInline, TransportExpenseInline, FoodExpenseInline, GenericExpenseInline]


class TicketInline(admin.StackedInline):
    model = Ticket
    extra = 0


class CarTripInline(admin.StackedInline):
    model = CarTrip
    extra = 0
    show_change_link = True


class TransportExpenseAdmin(admin.ModelAdmin):
    inlines = [TicketInline, CarTripInline]


class PassengerInline(admin.TabularInline):
    model = Passenger
    extra = 1


class CarTripAdmin(admin.ModelAdmin):
    inlines = [PassengerInline]


admin.site.register(Reimbursement, ReimbursementAdmin)
admin.site.register(TransportExpense, TransportExpenseAdmin)
admin.site.register(CarTrip, CarTripAdmin)
