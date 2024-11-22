from decimal import Decimal
from django.db import models
from django.utils.translation import gettext_lazy as _

from reimbursements.models import Reimbursement


class TransportExpense(models.Model):
    class Direction(models.TextChoices):
        INBOUND = "inbound", _("Inbound")
        OUTBOUND = "outbound", _("Outbound")
        ONSITE = "onsite", _("On Site")

    class Mode(models.TextChoices):
        CAR = "car", _("Car")
        BIKE = "bike", _("Bike")
        PUBLIC = "public", _("Public Transport")
        PLAN = "plan", _("Public Transport Plan")

    reimbursement = models.ForeignKey(
        Reimbursement,
        on_delete=models.CASCADE,
        related_name="transport",
        verbose_name=_("Reimbursement"),
    )
    direction = models.CharField(_("Direction"), max_length=8, choices=Direction)
    order = models.IntegerField(_("Order"))
    origin = models.CharField(_("Origin"), max_length=255)
    destination = models.CharField(_("Destination"), max_length=255)
    mode = models.CharField(_("Transport Mode"), max_length=8, choices=Mode)
    distance = models.DecimalField(
        _("Distance"), max_digits=10, decimal_places=2, null=True, blank=True
    )

    @property
    def amount(self):
        if self.reimbursement.type == Reimbursement.Type.COURSE:
            if self.mode == self.Mode.CAR:
                num_passengers = 1 + self.car_trip.passengers.count()
                return self.distance * Decimal(max(num_passengers, 6) * 0.05)
            elif self.mode == self.Mode.PUBLIC:
                if self.ticket.discount == Ticket.Discount.BAHN_CARD_25:
                    return self.ticket.price * Decimal(1.05)
                elif self.ticket.discount == Ticket.Discount.NO_DISCOUNT:
                    return self.ticket.price * Decimal(1.1)
                return self.ticket.price
            elif self.mode == self.Mode.BIKE:
                return self.distance * Decimal(0.13)
            elif self.mode == self.Mode.PLAN:
                return Decimal(12.25)
        elif self.reimbursement.type == Reimbursement.Type.COMMITTEE:
            if self.mode == self.Mode.CAR:
                num_passengers = 1 + self.car_trip.passengers.count()
                if num_passengers > 3:
                    return self.distance * Decimal(0.3)
                if num_passengers > 2:
                    return self.distance * Decimal(0.27)
                return self.distance * Decimal(0.2)
            elif self.mode == self.Mode.PUBLIC:
                return self.ticket.price
            elif self.mode == self.Mode.BIKE:
                return self.distance * Decimal(0.13)
            elif self.mode == self.Mode.PLAN:
                return Decimal(12.25)
        
        return Decimal(0)
        

    def __str__(self) -> str:
        direction = self.Direction(self.direction).label
        return _("%(direction)s from %(origin)s to %(destination)s") % {
            "direction": direction,
            "origin": self.origin,
            "destination": self.destination,
        }

    class Meta:
        ordering = ["reimbursement", "direction", "order"]
        verbose_name = _("Transport Expense")
        verbose_name_plural = _("Transport Expenses")


class Ticket(models.Model):
    class Discount(models.TextChoices):
        BAHN_CARD_25 = "BC25", _("BahnCard 25")
        BAHN_CARD_50 = "BC50", _("BahnCard 50")
        NO_DISCOUNT = "none", _("No Discount")

    expense = models.OneToOneField(
        TransportExpense, on_delete=models.CASCADE, verbose_name=_("Transport Expense")
    )
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)
    discount = models.CharField(_("Discount"), max_length=4, choices=Discount)

    def __str__(self) -> str:
        return _("Ticket for %(expense)s") % {"expense": self.expense}

    class Meta:
        verbose_name = _("Train Expense")
        verbose_name_plural = _("Train Expenses")


class CarTrip(models.Model):
    class Engine(models.TextChoices):
        COMBUSTION = "combustion", _("Combustion")
        ELECTRIC = "electric", _("Electric")
        HYBRID = "plug-in-hybrid", _("Hybrid")

    expense = models.OneToOneField(
        TransportExpense,
        on_delete=models.CASCADE,
        related_name="car_trip",
        verbose_name=_("Transport Expense"),
    )
    engine = models.CharField(_("Engine Type"), max_length=16, choices=Engine)

    def __str__(self) -> str:
        return _("Car Trip for %(expense)s") % {"expense": self.expense}

    class Meta:
        verbose_name = _("Car Expense")
        verbose_name_plural = _("Car Expenses")


class Passenger(models.Model):
    car_trip = models.ForeignKey(
        CarTrip, on_delete=models.CASCADE, related_name="passengers", verbose_name=_("Car Trip")
    )
    name = models.CharField(_("Name"), max_length=255)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("Passenger")
        verbose_name_plural = _("Passengers")


class FoodExpense(models.Model):
    class Absence(models.TextChoices):
        FULL_DAY = "full", _("Full Day")
        TRAVEL_DAY = "travel", _("Travel Day")
        SINGLE_DAY = "single", _("Single Day")

    reimbursement = models.ForeignKey(
        Reimbursement,
        on_delete=models.CASCADE,
        related_name="food",
        verbose_name=_("Reimbursement"),
    )
    date = models.DateField(_("Date"))
    absence = models.CharField(_("Absence"), max_length=8, choices=Absence)
    breakfast = models.BooleanField(_("Breakfast"))
    lunch = models.BooleanField(_("Lunch"))
    dinner = models.BooleanField(_("Dinner"))

    @property
    def amount(self):
        amount = 14
        if self.absence == self.Absence.FULL_DAY:
            amount = 28
        if self.breakfast:
            amount -= 5.6
        if self.lunch:
            amount -= 11.2
        if self.dinner:
            amount -= 11.2
        return Decimal(max(amount, 0))
    
    @property
    def meals(self):
        return [self.breakfast, self.lunch, self.dinner]

    def __str__(self) -> str:
        return _("Food Expense for %(date)s") % {"date": self.date}

    class Meta:
        ordering = ["reimbursement", "date"]
        verbose_name = _("Food Expense")
        verbose_name_plural = _("Food Expenses")


class GenericExpense(models.Model):
    reimbursement = models.ForeignKey(
        Reimbursement,
        on_delete=models.CASCADE,
        related_name="generic",
        verbose_name=_("Reimbursement"),
    )
    date = models.DateField(_("Date"))
    purpose = models.CharField(_("Purpose"), max_length=255)
    amount = models.DecimalField(_("Amount"), max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return self.purpose

    class Meta:
        ordering = ["reimbursement", "date"]
        verbose_name = _("Generic Expense")
        verbose_name_plural = _("Generic Expenses")
