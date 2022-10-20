from django.http import HttpResponse
from rest_framework.viewsets import ViewSet,ReadOnlyModelViewSet
from django.shortcuts import render
#from database_site.models import Location,Taxon,Lifestage,Sex,Ai,Tasks,Annotators,Deployments,Event,Media,Observation,Occurence,Behavior,Grades
from database_site.models import *
from database_site.models_queryObjects import *
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
from django.core import serializers
from datetime import datetime, timedelta
import pytz
from rest_framework.permissions import IsAuthenticated
utc=pytz.UTC



class TaxonViewSet(viewsets.ModelViewSet):
    queryset = Taxon.objects.all().order_by('genericname')
    serializer_class = TaxonSerializer

class AiViewSet(viewsets.ModelViewSet):
    queryset = Ai.objects.all().order_by('aiid')
    serializer_class = AiSerializer

class LocationViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Location.objects.all().order_by('locationid')
    serializer_class = LocationSerializer
        
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


class DeploymentListView(generics.ListAPIView):
    queryset = Deployments.objects.all()#.order_by('deploymentid')
    serializer_class = DeploymentsSerializer(queryset, many = True)

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    

class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all().order_by('sequenceid')
    serializer_class = MediaSerializer
 

class ObservationViewSet(viewsets.ModelViewSet):
    queryset = Observation.objects.all().order_by('sequenceid')
    serializer_class = ObservationSerializer



class OccurenceViewSet(viewsets.ModelViewSet):
    queryset = Occurence.objects.all()
    serializer_class = OccurenceSerializer


    def create(self, request):
        imgs = Occurence.objects.filter(eventid__eventdate__range = [request.data['start'], request.data['end']]).filter(taxonid__genericname = request.data['animal']).filter(eventid__eventid__deploymentid__cameraid =  request.data['cameraid'])

        print(imgs)
        return JsonResponse(serializers.serialize('json', imgs), safe=False)

    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = '__all__'

class BehaviorViewSet(viewsets.ModelViewSet):
    queryset = Behavior.objects.all().order_by('behaviorid')
    serializer_class = BehaviorSerializer

class GradesViewSet(viewsets.ModelViewSet):
    queryset = Grades.objects.all().order_by('grade')
    serializer_class = GradesSerializer

"""
class GetImg(viewsets.ModelViewSet):
    queryset = Observation.objects.all()
    serializer_class = ObservationSerializer
    #filterset_fields = ('animal')
    
    #def retrieve(self, request, *args, **kwargs):
        #img = Observation.objects.select_related().filter(mediaid = args['cameraid'])
        #serializer = ObservationSerializer(img)
        #return(img)




class FiltByChoiceManager(django_filters.FilterSet):
    from_start = django_filters.DateTimeFilter(field_name = "start", lookup_type='gte')
    to_end = django_filters.DateTimeFilter(field_name = "end", lookup_type='lte')
    animal = django_filters.CharFilter(field_name = 'animal', lookup_type='exact')
    cameraid = django_filters.CharFilter(field_name = 'cameraid', lookup_type='exact')
    
    class Meta:
        model = FetchImages
        fields = '__all__'

#class FilterByChoiceViewSet(ReadOnlyModelViewSet):
#    queryset = FetchImages.objects.all()
    #serializer_class=FetchImagesSerializer
    #serializer_class = FetchImagesSerializer
    #def Get(request,animal):
        #Result = queryset.filter(animal=animal)
        #serializer = FetchImagesSerializer(Result)
        #return Response(serializer.data)
    #def list(self, request):
        #serializer = FetchImagesSerializer(self.queryset, many=True)
        #return Response(serializer.data)

#    def retrieve(self, request, *args, **kwargs):
#        img = FetchImages.objects.filter(animal = args['animal'])
#        serializer = FetchImagesSerializer(img)
#        return Response(serializer)
        #get_object_or_404(self.queryset,animal = "WOLF")
        #serializer = FetchImagesSerializer(img)
        #return Response(serializer.data)

    #@api_view(['GET','PUT','DELETE'])
    #def GetImg(request,animal):
        #try:
            #Result = FetchImages.objects.filter(animal=animal)
        #except FetchImages.DoesNotExist:
            #return Response(status=HTTP_404_NOT_FOUND)
        #if request.method == 'GET':
            #serializer = FetchImagesSerializer(Result)
            #return Response(serializer.data)
#class FilterByChoiceViewSet(generics.ListCreateAPIView):
    #queryset = FetchImages.objects.all()
    #queryset = FetchImages.objects.filter(start__range=["start", "end"])
    #filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    #filter_class = FiltByChoiceManager
    #serializer_class = FetchImagesSerializer
    #name = 'robot-list'
    #filterset_fields = ['animal','start']


    def list(self, request, animal = None):
        if animal == None:
            images = FetchImages.objects.filter(animal="WOLF")
        else:
            images = models.Product.objects.filter(animal = 'WOLF')
        images = self.filter_queryset(images)
        page = self.paginate_queryset(images)

        serializer = self.get_serializer(page, many=True)
        result_set = serializer.data
        return Response(result_set)



    def get_result_set(self, images):
        result_set = serializers.FetchImagesSerializer(images, many=True).data
        return result_set
   
    #filterset_fields = ''
    #def FetchImg(self,cameraid,animal,start,end):
        #queryset = Media.objects.filter(timestamp__range = [start,end])
        #queryset = FetchImages.objects.filter(animal=animal)
        #return Response(res)
    
    #filter_backends = [django_filters.rest_framework.DjangoFilterBackend]#,django_filters.rest_framework.OrderingFilter]
    #filterset_fields = ['cameraid', 'start', 'end', 'animal']
    #filterset_fields = ['animal','start']
    

    #def my_custom_filter(self, queryset, cameraid, animel):
        #eturn queryset.filter(**{
    #filter_backends = [django_filters.rest_framework.DjangoFilterBackend] #,django_filters.IsoDateTimeFilter]
    #filterset_fields = ['cameraid', 'start', 'end', 'animal']
    #queryset = get_queryset()
    #def get_queryset(self):
        #queryset = FetchImages.objects.all()
        #animal = self.request.query_params.get('animal')
        #if animal is not None:
            #queryset = queryset.filter(animal_animal=animal)
        #return queryset

    #queryset = get_queryset
    #def FetchImg(self, cameraid,start,end,animal):
        #start = start.replace(tzinfo=utc)
        #end = end.replace(tzinfo=utc)
        #raise ValidationError(queryset.last().start)
        #res = FetchImages.objects.filter(cameraid = cameraid).filter(animal = animal).filter(start = start).filter(end=end)#.filter(start__lte = end)#.filter(end__ilte=end)
        
        #return Response(res)
    




@api_view(['GET','PUT','DELETE'])
def GetImages(request,animal,cameraid,start,end):
    try:
        Result = FetchImages.objects.get(animal=animal, cameraid=cameria, start__gte=start, end__lte=end)
    #filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    #filterset_fields = ['animal','cameraid', 'start', 'end']
    except FetchImages.DoesNotExist:
        return Response(status=HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = FetchImagesSerializer(Result)
        return Response(serializer.data)



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
