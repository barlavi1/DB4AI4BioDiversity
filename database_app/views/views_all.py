from database_site.models import *
from rest_framework import permissions
from rest_framework.response import Response
from .cust_view import *
from ..serializers import *
from django.shortcuts import get_object_or_404

class SexViewSet(NoDeleteViewSet):
    queryset = Sex.objects.all()
    serializer_class = SexSerializer
    permission_classes = [permissions.IsAuthenticated]


class TaxonViewSet(NoDeleteViewSet):
    queryset = Taxon.objects.all()
    serializer_class = TaxonSerializer
    permission_classes = [permissions.IsAuthenticated]


class BehaviorViewSet(NoDeleteViewSet):
    queryset = Behavior.objects.all()
    serializer_class = BehaviorSerializer
    permission_classes = [permissions.IsAuthenticated]


class LifestageViewSet(NoDeleteViewSet):
    queryset = Lifestage.objects.all()
    serializer_class = LifestageSerializer
    permission_classes = [permissions.IsAuthenticated]


class CountyViewSet(NoDeleteViewSet):
    queryset = County.objects.all()
    serializer_class = CountySerializer
    permission_classes = [permissions.IsAuthenticated]


#class RegionViewSet(NoDeleteViewSet):
#    queryset = Region.objects.all()
#    serializer_class = RegionSerializer
#    permission_classes = [permissions.IsAuthenticated]

class LocationViewSet(NoDeleteViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [permissions.IsAuthenticated]

class DeploymentViewSet(NoDeleteViewSet):
    queryset = Deployment.objects.all()
    serializer_class = DeploymentSerializer
    permission_classes = [permissions.IsAuthenticated]

class EventViewSet(NoDeleteViewSet):#(NoDeleteViewSet):#NoDeleteViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    #def list(self, request):
        #queryset = Event.objects.all()
        #serializer = EventSerializer(queryset, many=True)
        #return Response(serializer.data)

    #def retrieve(self, request, pk=None):
        #queryset = Event.objects.all()
        #event = get_object_or_404(queryset, eventid=pk)
        #serializer = EventSerializer(event)
        #return Response(serializer.data)


class ImageViewSet(NoDeleteViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated]

class OccurrenceViewSet(NoDeleteViewSet):
    queryset = Occurrence.objects.all()
    serializer_class = OccurrenceSerializer
    permission_classes = [permissions.IsAuthenticated]

class SequenceViewSet(NoDeleteViewSet):
    queryset = Sequence.objects.all()
    serializer_class = SequenceSerializer
    permission_classes = [permissions.IsAuthenticated]

class VideoViewSet(NoDeleteViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated]


