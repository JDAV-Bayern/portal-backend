from rest_framework import serializers

from contact_info.models import Address, BankAccount, Country, Locality


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name']


class LocalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Locality
        fields = ['postal_code', 'name', 'country']


class AddressSerializer(serializers.ModelSerializer):
    postal_code = serializers.CharField(source='locality.postal_code')
    locality = serializers.CharField(source='locality.name')
    country = serializers.PrimaryKeyRelatedField(source='locality.country', queryset=Country.objects.all())

    class Meta:
        model = Address
        fields = ['line1', 'line2', 'postal_code', 'locality', 'country']


class BankAccountSerializer(serializers.Serializer):
    class Meta:
        model = BankAccount
        fields = ['iban', 'bic']
