from rest_framework import generics

from contact_info.models import Country, Locality
from contact_info.serializers import CountrySerializer, LocalitySerializer


class CountryList(generics.ListAPIView):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()


class LocalityList(generics.ListAPIView):
    serializer_class = LocalitySerializer

    def get_queryset(self):
        postal_code = self.request.query_params.get('postal_code', None)
        if postal_code:
            return Locality.objects.filter(postal_code=postal_code, is_admin_provided=True)
        return Locality.objects.none()
