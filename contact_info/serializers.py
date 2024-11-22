from rest_framework import serializers

from contact_info.models import Address, BankAccount, Country, Locality


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name']


class LocalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Locality
        fields = ['postal_code', 'name', 'country_id']
