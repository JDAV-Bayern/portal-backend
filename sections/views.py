from rest_framework import generics

from sections.models import Federation, Section
from sections.serializers import FederationSerializer, SectionSerializer


class FederationList(generics.ListAPIView):
    queryset = Federation.objects.all()
    serializer_class = FederationSerializer

class FederationDetail(generics.RetrieveAPIView):
    queryset = Federation.objects.all()
    serializer_class = FederationSerializer

class SectionList(generics.ListAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

class SectionDetail(generics.RetrieveAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
