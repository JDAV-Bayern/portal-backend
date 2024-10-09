from rest_framework import serializers

from contact_info.models import Locality
from courses.models import Course
from people.models import Person, PersonAddress, PersonBankAccount
from people.serializers import PersonSerializer
from reimbursements.models import (
    CarTrip,
    CourseDetails,
    FoodExpense,
    GenericExpense,
    Reimbursement,
    Ticket,
    TransportExpense,
    TravelDetails,
)
from reimbursements.models.expenses import Passenger


class NameRelatedField(serializers.RelatedField):
    def to_internal_value(self, data):
        return {"name": data}

    def to_representation(self, value):
        return value.name


class TravelDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelDetails
        fields = ["purpose", "location", "start_date", "end_date"]


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["price", "discount"]


class CarTripSerializer(serializers.ModelSerializer):
    passengers = NameRelatedField(many=True, queryset=Passenger.objects.all())

    class Meta:
        model = CarTrip
        fields = ["engine", "passengers"]


class TransportExpenseSerializer(serializers.ModelSerializer):
    ticket = TicketSerializer(required=False)
    car_trip = CarTripSerializer(required=False)

    def validate(self, attrs):
        if attrs.get("mode") == TransportExpense.Mode.CAR and not attrs.get("car_trip"):
            raise serializers.ValidationError(
                {"car_trip": "This field is required when mode is car"}
            )
        if attrs.get("mode") != TransportExpense.Mode.CAR and attrs.get("car_trip"):
            raise serializers.ValidationError(
                {"car_trip": "This field is not required when mode is not car"}
            )
        if attrs.get("mode") == TransportExpense.Mode.PUBLIC and not attrs.get(
            "ticket"
        ):
            raise serializers.ValidationError(
                {"ticket": "This field is required when mode is public"}
            )
        if attrs.get("mode") != TransportExpense.Mode.PUBLIC and attrs.get("ticket"):
            raise serializers.ValidationError(
                {"ticket": "This field is not required when mode is not public"}
            )
        return attrs

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return {key: value for key, value in rep.items() if value is not None}

    class Meta:
        model = TransportExpense
        fields = [
            "direction",
            "origin",
            "destination",
            "mode",
            "distance",
            "ticket",
            "car_trip",
        ]


class FoodExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodExpense
        fields = ["date", "absence", "breakfast", "lunch", "dinner"]


class GenericExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenericExpense
        fields = ["date", "purpose", "amount"]


class ReimbursementSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(
        source="course_details.course", queryset=Course.objects.all(), required=False
    )
    travel_details = TravelDetailsSerializer(required=False)

    participant = PersonSerializer()

    transport = TransportExpenseSerializer(many=True)
    food = FoodExpenseSerializer(many=True, required=False)
    generic = GenericExpenseSerializer(many=True, required=False)

    class Meta:
        model = Reimbursement
        fields = [
            "id",
            "type",
            "course",
            "travel_details",
            "participant",
            "transport",
            "food",
            "generic",
            "note",
        ]

    def validate(self, attrs):
        errors = {}

        if attrs.get("type") == Reimbursement.Type.COURSE:
            errors = {}
            if not attrs.get("course_details"):
                print(attrs)
                errors["course"] = "This field is required when type is course"
            if attrs.get("travel_details"):
                errors["travel_details"] = (
                    "This field is not required when type is course"
                )
            if attrs.get("food"):
                errors["food"] = "This field is not required when type is course"
            if attrs.get("generic"):
                errors["generic"] = "This field is not required when type is course"
        elif attrs.get("type") == Reimbursement.Type.COMMITTEE:
            if not attrs.get("travel_details"):
                errors["travel_details"] = (
                    "This field is required when type is committee"
                )
            if attrs.get("course_details"):
                errors["course"] = "This field is not required when type is committee"

        if errors:
            raise serializers.ValidationError(errors)

        return attrs

    def create(self, validated_data):
        course_details_data = validated_data.pop("course_details", None)
        travel_details_data = validated_data.pop("travel_details", None)
        participant_data = validated_data.pop("participant")
        transport_data = validated_data.pop("transport")
        food_data = validated_data.pop("food", [])
        generic_data = validated_data.pop("generic", [])

        participant = self.create_person(participant_data)
        reimbursement = Reimbursement.objects.create(
            participant=participant, **validated_data
        )

        if course_details_data:
            CourseDetails.objects.create(reimbursement=reimbursement, **course_details_data)
        if travel_details_data:
            TravelDetails.objects.create(
                reimbursement=reimbursement, **travel_details_data
            )

        self.create_transport_expenses(reimbursement, transport_data)
        for food_expense in food_data:
            FoodExpense.objects.create(reimbursement=reimbursement, **food_expense)
        for generic_expense in generic_data:
            GenericExpense.objects.create(
                reimbursement=reimbursement, **generic_expense
            )

        return reimbursement

    def create_person(self, validated_data):
        address_data = validated_data.pop("address")
        bank_account_data = validated_data.pop("bank_account")

        person = Person.objects.create(**validated_data)

        locality_data = address_data.pop("locality")
        locality, _ = Locality.objects.get_or_create(**locality_data)
        PersonAddress.objects.create(person=person, locality=locality, **address_data)

        PersonBankAccount.objects.create(person=person, **bank_account_data)

        return person

    def create_transport_expenses(self, reimbursement, validated_data):
        for index, transport_data in enumerate(validated_data):
            car_trip_data = transport_data.pop("car_trip", None)
            ticket_data = transport_data.pop("ticket", None)

            expense = TransportExpense.objects.create(
                reimbursement=reimbursement, order=index, **transport_data
            )

            if car_trip_data:
                passengers_data = car_trip_data.pop("passengers")
                car_trip = CarTrip.objects.create(expense=expense, **car_trip_data)
                for passenger_data in passengers_data:
                    Passenger.objects.create(car_trip=car_trip, **passenger_data)

            if ticket_data:
                Ticket.objects.create(expense=expense, **ticket_data)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return {key: value for key, value in rep.items() if value is not None}
