from rest_framework import serializers

from sections.models import Federation, Section


class FederationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Federation
        fields = ('id', 'type', 'name', 'parent')

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ('id', 'number', 'name', 'state', 'district')
