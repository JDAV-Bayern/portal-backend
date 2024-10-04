from rest_framework import serializers

from contact_info.models import Country
from people.models import Person, PersonAddress, PersonBankAccount


class AddressSerializer(serializers.ModelSerializer):
    postal_code = serializers.CharField(source='locality.postal_code')
    locality = serializers.CharField(source='locality.name')
    country = serializers.PrimaryKeyRelatedField(source='locality.country', queryset=Country.objects.all())

    class Meta:
        model = PersonAddress
        fields = ['line1', 'line2', 'postal_code', 'locality', 'country']


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonBankAccount
        fields = ['iban', 'bic']


class PersonSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    bank_account = BankAccountSerializer()

    class Meta:
        model = Person
        fields = ['given_name', 'family_name', 'section', 'email', 'address', 'bank_account']
