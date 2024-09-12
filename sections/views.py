from django.shortcuts import get_object_or_404
from rest_framework import generics

from sections.models import Federation, Section
from sections.serializers import FederationSerializer, SectionSerializer


class FederationList(generics.ListAPIView):
    queryset = Federation.objects.all()
    serializer_class = FederationSerializer

class FederationDetail(generics.RetrieveAPIView):
    queryset = Federation.objects.all()
    serializer_class = FederationSerializer

class FederationSectionList(generics.ListAPIView):
    serializer_class = SectionSerializer

    def get_queryset(self):
        federation = get_object_or_404(Federation, pk=self.kwargs['federation_id'])
        if federation.type == Federation.NATIONAL:
            return Section.objects.all()
        elif federation.type == Federation.STATE:
            return Section.objects.filter(state=federation)
        elif federation.type == Federation.DISTRICT:
            return Section.objects.filter(district=federation)
        else:
            return Section.objects.none()

class SectionList(generics.ListAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

class SectionDetail(generics.RetrieveAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
