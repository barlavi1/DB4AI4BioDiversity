#import glob
#from django.http import HttpResponse
#from rest_framework.viewsets import ViewSet,ReadOnlyModelViewSet
#from django.shortcuts import render
#from database_site.models import *
#from django_filters.rest_framework import DjangoFilterBackend
#from rest_framework import generics
from rest_framework.serializers import *
from rest_framework import viewsets
#from rest_framework.views import APIView
from .serializers import *
from .Objects import *
#from django.http.response import JsonResponse
#from rest_framework.parsers import JSONParser 
#from rest_framework import status
#import django_filters.rest_framework
#from rest_framework import filters
#import pandas as pd
#from rest_framework.response import Response
#from django.core import serializers
#from datetime import datetime, timedelta
#import pytz
#from rest_framework.permissions import IsAuthenticated
#utc=pytz.UTC
from rest_framework import permissions
#import django.contrib.auth.models
#from .models import Videos
#from .ModelForm import VideoForm
#from django.template import loader
#from .settings import TEMPLATE_DIRS
#class TaxonViewSet(viewsets.ModelViewSet):
#    queryset = Taxon.objects.all().order_by('genericname')
#    serializer_class = TaxonSerializer

#class AiViewSet(viewsets.ModelViewSet):
#    queryset = Ai.objects.all().order_by('aiid')
#    serializer_class = AiSerializer

#class LocationViewSet(viewsets.ModelViewSet):
    #permission_classes = (IsAuthenticated,)
    #queryset = Location.objects.all().order_by('locationid')
    #serializer_class = LocationSerializer
        
#class LifestageViewSet(viewsets.ModelViewSet):
#    queryset = Lifestage.objects.all().order_by('lifestageid')
#    serializer_class = LifestageSerializer

#class SexViewSet(viewsets.ModelViewSet):
#    queryset = Sex.objects.all().order_by('sexid')
#    serializer_class = SexSerializer

#class TasksViewSet(viewsets.ModelViewSet):
#    queryset = Tasks.objects.all().order_by('taskid')
#    serializer_class = TasksSerializer

#class AnnotatorsViewSet(viewsets.ModelViewSet):
#    queryset = Annotators.objects.all().order_by('annotatorid')
#    serializer_class = AnnotatorsSerializer

#class DeploymentsViewSet(viewsets.ModelViewSet):
#    queryset = Deployments.objects.all()#.order_by('deploymentid')
#    serializer_class = DeploymentsSerializer

#    def create(self, request, *args, **kwargs):
#        many = isinstance(request.data, list)
#        serializer = self.get_serializer(data=request.data, many=many)
#        serializer.is_valid(raise_exception=True)
#        self.perform_create(serializer)
#        headers = self.get_success_headers(serializer.data)
#        return Response(serializer.data, headers=headers)


#class DeploymentListView(generics.ListAPIView):
#    queryset = Deployments.objects.all()#.order_by('deploymentid')
#    serializer_class = DeploymentsSerializer(queryset, many = True)

class EventViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class OccurenceViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Occurence.objects.all()
    serializer_class = OccurenceSerializer


class Video(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

class Image(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Image.objects.all()
    serializer_class = ImageSerializer




class AddOccurenceViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    def list(self, request):
        print ("##########OK########")
        queryset = Event.objects.all()
        UploadedDate = request.data['uploaded_date']
        EventPath = glob.glob(str(settings.BASE_DIR)+"/media/images/"+request.data['camera']+"/"+request.data['location']+"/"+UploadedDate+"/*"+request.data['imgname'])[0]
        print (EventPath)
        #print (str(settings.BASE_DIR)+"/media/images/"+request.data['camera']+"/"+request.data['location']+"/"+"2022-11-24/*"+request.data['imgname'])
        EventPath = "/".join(EventPath.split("/")[5:])
        eventid = Event.objects.get(filepath=EventPath)
        behavior=Behavior.objects.get(behaviorid = 0)
        sex = Sex.objects.get(sexid=0)
        tax = Taxon.objects.get(genericname=request.data['animal'])
        lifestage = Lifestage.objects.all(lifestageid = 0)
        NewOccurence=Occurence(eventid=eventid, taxonid=tax, individualcount=1, sexid=sex, lifestageid=lifestage, behaviorid=behavior)
        NewOccurence.save()
        return Response({'queryset': {'ok':'ok'}})


