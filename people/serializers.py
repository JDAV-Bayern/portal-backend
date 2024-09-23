from rest_framework import serializers

from contact_info.serializers import AddressSerializer, BankAccountSerializer
from people.models import Person


class PersonSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    bank_account = BankAccountSerializer()

    class Meta:
        model = Person
        fields = ['given_name', 'family_name', 'section', 'email', 'address', 'bank_account']
