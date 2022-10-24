from django.http import HttpResponse
from rest_framework.viewsets import ViewSet,ReadOnlyModelViewSet
from django.shortcuts import render
#from database_site.models import Location,Taxon,Lifestage,Sex,Ai,Tasks,Annotators,Deployments,Event,Media,Observation,Occurence,Behavior,Grades
from database_site.models import *
#from database_site.models_queryObjects import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.serializers import *
from rest_framework import viewsets
from rest_framework.views import APIView
from .serializers import *
from .Objects import *
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
import csv


class TaxonViewSet(viewsets.ModelViewSet):
    queryset = Taxon.objects.all().order_by('genericname')
    serializer_class = TaxonSerializer

class AiViewSet(viewsets.ModelViewSet):
    queryset = Ai.objects.all().order_by('aiid')
    serializer_class = AiSerializer

class LocationViewSet(viewsets.ModelViewSet):
    #permission_classes = (IsAuthenticated,)
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
    

#class MediaViewSet(viewsets.ModelViewSet):
#    queryset = Media.objects.all().order_by('sequenceid')
#    serializer_class = MediaSerializer

 
#class ObservationViewSet(viewsets.ModelViewSet):
#    queryset = Observation.objects.all()
#    serializer_class = ObservationSerializer

class TEST_VIEW(viewsets.ViewSet):
    
    def list(self, request):
        MediaData = []
        queryset = Event.objects.all()
        for e in queryset:
            if 1==1:
                event_serializer = EventSerializer(e, many=False)
                event_info = dict(event_serializer.data)
                fileName = (str(e.filepath).split("\\")[-1]).split("/")[-1]
                img = Image.open(e.filepath)
                filemediatype = img.format
                exif = {
                    PIL.ExifTags.TAGS[k]: v
                    for k, v in img._getexif().items()
                    if k in PIL.ExifTags.TAGS
                }
                img.close()
                print( e.eventdate)
                MediaData.append(MediaInfo(
                    mediaid=e.eventid,
                    deploymentid = e.deploymentid.deploymentid,
                    sequenceid=e.supraeventid,
                    capturemethod = e.samplingprotocol,
                    timestamp = e.eventdate,
                    filepath = str(e.filepath),
                    filemediatype = filemediatype,
                    exifdata = str(exif),
                    favourite='',
                    comments=e.eventremarks,
                    field_id=e.eventid
                ).__dict__)
            else:
                print("somethin is wrong with "+str(e.eventid)+ " " + str(e.filepath))
        return Response({'queryset': MediaData})


class GetImages(viewsets.ViewSet):
    def create(self, request):
        imgs = Occurence.objects.filter(eventid__eventdate__range = [request.data['start'], request.data['end']]).filter(taxonid__genericname = request.data['animal']).filter(eventid__deploymentid__cameraid =  request.data['cameraid'])        
        print(imgs)
        
        response = HttpResponse(
                content_type='text/csv',
                headers={'Content-Disposition': f'attachment; filename="test.csv"'}
            )
        #response['Content-Disposition'] = 'attachment; filename="file.csv"'
        writer = csv.writer(response, quoting=csv.QUOTE_NONE, escapechar = ' ')


        imgsData = []
        supraEventIDs = []
        max_images = 0
        #supraEventIDs_dict = dict()
        for img in imgs:
            supraEventIDs.append(Event.objects.get(eventid=img.eventid.eventid).supraeventid)
        supraEventIDs = set(supraEventIDs)
        for supraeventid in supraEventIDs:
            imgs_cluster = Occurence.objects.filter(eventid__eventdate__range = [request.data['start'], request.data['end']]).filter(taxonid__genericname = request.data['animal']).filter(eventid__deploymentid__cameraid =  request.data['cameraid']).filter(eventid__supraeventid = supraeventid)
            num_images = len(imgs_cluster)
            if num_images > max_images:
                max_images = num_images
        header = []
        header.append("id")
        for i in range(max_images):
            header.append("image"+str(i+1))
        header.append("start")
        header.append("end")
        writer.writerow(header)
        for supraeventid in supraEventIDs:
            start = Event.objects.filter(supraeventid = supraeventid).order_by('eventdate')[0].eventdate
            end = Event.objects.filter(supraeventid = supraeventid).order_by('-eventdate')[0].eventdate
            imgs_cluster = Occurence.objects.filter(eventid__eventdate__range = [request.data['start'], request.data['end']]).filter(taxonid__genericname = request.data['animal']).filter(eventid__deploymentid__cameraid =  request.data['cameraid']).filter(eventid__supraeventid = supraeventid)
            #img_cluster = imgs.objects.select_related('Event').filter(event__eventid__supraeventid = supraeventi
            FilePaths= []            
            for im in imgs_cluster:
                img_filePath = (str(im.eventid.filepath).split("\\")[-1]).split("/")[-1]
                FilePaths.append(str(img_filePath))
            num_images = len(FilePaths)
            FilePaths = ",".join(FilePaths) + ","*(max_images-num_images)
            print(FilePaths)
            #print(start,end,request.data['cameraid'],request.data['animal'],FilePaths,supraeventid)
            imgsData.append(ImgInfo(
                start = start,
                end = end,
                cameraid = request.data['cameraid'],
                animal = request.data['animal'],
                imgName = FilePaths,
                supraeventid = supraeventid
            ).__dict__)
           # print(imgsData)
            writer.writerow([supraeventid,FilePaths,start,end])
        return response 
        #return Response({'queryset': imgsData})
        #return JsonResponse(serializers.serialize('json', imgsData), safe=False)

class OccurenceViewSet(viewsets.ModelViewSet):
    queryset = Occurence.objects.all()
    serializer_class = OccurenceSerializer

class BehaviorViewSet(viewsets.ModelViewSet):
    queryset = Behavior.objects.all().order_by('behaviorid')
    serializer_class = BehaviorSerializer

class GradesViewSet(viewsets.ModelViewSet):
    queryset = Grades.objects.all().order_by('grade')
    serializer_class = GradesSerializer

class PreUploadViewSet(viewsets.ModelViewSet):
    queryset = PreUpload.objects.all()
    serializer_class = PreUploadSerializer

"""
class getimg(viewsets.modelviewset):
    queryset = observation.objects.all()
    serializer_class = observationserializer
    #filterset_fields = ('animal')
    
    #def retrieve(self, request, *args, **kwargs):
        #img = observation.objects.select_related().filter(mediaid = args['cameraid'])
        #serializer = observationserializer(img)
        #return(img)




class filtbychoicemanager(django_filters.filterset):
    from_start = django_filters.datetimefilter(field_name = "start", lookup_type='gte')
    to_end = django_filters.datetimefilter(field_name = "end", lookup_type='lte')
    animal = django_filters.charfilter(field_name = 'animal', lookup_type='exact')
    cameraid = django_filters.charfilter(field_name = 'cameraid', lookup_type='exact')
    
    class meta:
        model = fetchimages
        fields = '__all__'

#class filterbychoiceviewset(readonlymodelviewset):
#    queryset = fetchimages.objects.all()
    #serializer_class=fetchimagesserializer
    #serializer_class = fetchimagesserializer
    #def get(request,animal):
        #result = queryset.filter(animal=animal)
        #serializer = fetchimagesserializer(result)
        #return response(serializer.data)
    #def list(self, request):
        #serializer = fetchimagesserializer(self.queryset, many=true)
        #return response(serializer.data)

#    def retrieve(self, request, *args, **kwargs):
#        img = fetchimages.objects.filter(animal = args['animal'])
#        serializer = fetchimagesserializer(img)
#        return response(serializer)
        #get_object_or_404(self.queryset,animal = "wolf")
        #serializer = fetchimagesserializer(img)
        #return response(serializer.data)

    #@api_view(['get','put','delete'])
    #def getimg(request,animal):
        #try:
            #result = fetchimages.objects.filter(animal=animal)
        #except fetchimages.doesnotexist:
            #return response(status=http_404_not_found)
        #if request.method == 'get':
            #serializer = fetchimagesserializer(result)
            #return response(serializer.data)
#class filterbychoiceviewset(generics.listcreateapiview):
    #queryset = fetchimages.objects.all()
    #queryset = fetchimages.objects.filter(start__range=["start", "end"])
    #filter_backends = [django_filters.rest_framework.djangofilterbackend]
    #filter_class = filtbychoicemanager
    #serializer_class = fetchimagesserializer
    #name = 'robot-list'
    #filterset_fields = ['animal','start']


    def list(self, request, animal = none):
        if animal == none:
            images = fetchimages.objects.filter(animal="wolf")
        else:
            images = models.product.objects.filter(animal = 'wolf')
        images = self.filter_queryset(images)
        page = self.paginate_queryset(images)

        serializer = self.get_serializer(page, many=true)
        result_set = serializer.data
        return response(result_set)



    def get_result_set(self, images):
        result_set = serializers.fetchimagesserializer(images, many=true).data
        return result_set
   
    #filterset_fields = ''
    #def fetchimg(self,cameraid,animal,start,end):
        #queryset = media.objects.filter(timestamp__range = [start,end])
        #queryset = fetchimages.objects.filter(animal=animal)
        #return response(res)
    
    #filter_backends = [django_filters.rest_framework.djangofilterbackend]#,django_filters.rest_framework.orderingfilter]
    #filterset_fields = ['cameraid', 'start', 'end', 'animal']
    #filterset_fields = ['animal','start']
    

    #def my_custom_filter(self, queryset, cameraid, animel):
        #eturn queryset.filter(**{
    #filter_backends = [django_filters.rest_framework.djangofilterbackend] #,django_filters.isodatetimefilter]
    #filterset_fields = ['cameraid', 'start', 'end', 'animal']
    #queryset = get_queryset()
    #def get_queryset(self):
        #queryset = fetchimages.objects.all()
        #animal = self.request.query_params.get('animal')
        #if animal is not none:
            #queryset = queryset.filter(animal_animal=animal)
        #return queryset

    #queryset = get_queryset
    #def fetchimg(self, cameraid,start,end,animal):
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
