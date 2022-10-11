from django.http import HttpResponse
from django.shortcuts import render
#from database_site.models import Location,Taxon,Lifestage,Sex,Ai,Tasks,Annotators,Deployments,Event,Media,Observation,Occurence,Behavior,Grades
from database_site.models import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.serializers import *
from rest_framework import viewsets
from .serializers import *
#from .serializers import TaxonSerializer, AiSerializer,LifestageSerializer,SexSerializer,LocationSerializer,TasksSerializer,AnnotatorsSerializer,DeploymentsSerializer,MediaSerializer,ObservationSerializer,OccurenceSerializer,BehaviorSerializer,GradesSerializer,EventSerializer
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
import django_filters.rest_framework
from rest_framework import filters
import pandas as pd
from rest_framework.response import Response

# Create your views here.



class TaxonViewSet(viewsets.ModelViewSet):
    queryset = Taxon.objects.all().order_by('genericname')
    serializer_class = TaxonSerializer

class AiViewSet(viewsets.ModelViewSet):
    queryset = Ai.objects.all().order_by('aiid')
    serializer_class = AiSerializer

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all().order_by('locationid')
    serializer_class = LocationSerializer
    
    #def create(self, request, *args, **kwargs):
        #serializer = self.get_serializer(data=request.data)
        #serializer.is_valid(raise_exception=True)
        #obj = self.perform_create(serializer)
        #headers = self.get_success_headers(serializer.data)
        #return Response(self.get_serializer(obj).data, status=status.HTTP_201_CREATED, headers=headers)

    #def perform_create(self, serializer):
        #return serializer.save(host=self.request.user)

class LifestageViewSet(viewsets.ModelViewSet):
    queryset = Lifestage.objects.all().order_by('lifestageid')
    serializer_class = LifestageSerializer

class SexViewSet(viewsets.ModelViewSet):
    queryset = Sex.objects.all().order_by('sexid')
    serializer_class = SexSerializer

class TasksViewSet(viewsets.ModelViewSet):
    queryset = Tasks.objects.all().order_by('taskid')
    serializer_class = TasksSerializer

class AnnotatorsViewSet(viewsets.ModelViewSet):
    queryset = Annotators.objects.all().order_by('annotatorid')
    serializer_class = AnnotatorsSerializer

class DeploymentsViewSet(viewsets.ModelViewSet):
    queryset = Deployments.objects.all()#.order_by('deploymentid')
    serializer_class = DeploymentsSerializer

    def create(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, headers=headers)



    #def post(self,instance = None, data = None, many = False, partial = False):
        #return super(DeploymentsViewSet, self).post(instance=instance, many=True, data = data, partial=partial)

class DeploymentListView(generics.ListAPIView):
    queryset = Deployments.objects.all()#.order_by('deploymentid')
    serializer_class = DeploymentsSerializer(queryset, many = True)

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = '__all__'

class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all().order_by('sequenceid')
    serializer_class = MediaSerializer
    #filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    #filterset_fields = '__all__'

class ObservationViewSet(viewsets.ModelViewSet):
    queryset = Observation.objects.all().order_by('sequenceid')
    serializer_class = ObservationSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = '__all__'

class OccurenceViewSet(viewsets.ModelViewSet):
    queryset = Occurence.objects.all()
    serializer_class = OccurenceSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = '__all__'

class BehaviorViewSet(viewsets.ModelViewSet):
    queryset = Behavior.objects.all().order_by('behaviorid')
    serializer_class = BehaviorSerializer

class GradesViewSet(viewsets.ModelViewSet):
    queryset = Grades.objects.all().order_by('grade')
    serializer_class = GradesSerializer




"""
class LocationListView(generics.ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields =['locationid', 'country']


@api_view(['GET','PUT','DELETE'])
def GetEvent(request,taxon,pk_location,start,end):
    try:
        Result = Observation.objects.get(taxonid=taxon, locationid=deploymentid.locationid, timestamp>=start, timestamp<=end)
    except Observation.DoesNotExist:
        return Response(status=HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ObservationSerializer(Result)
        return Response(serializer.data)



@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk):

#    Retrieve, update or delete a code snippet.

    try:
        loc = Location.objects.get(pk=pk)
    except Location.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = LocationSerializer(snippet)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = LocationSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        loc.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
"""
