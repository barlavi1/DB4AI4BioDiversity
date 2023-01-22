from django.http import HttpResponse
from rest_framework.viewsets import ViewSet
#from django.shortcuts import render
#from database_site.models import Location,Taxon,Lifestage,Sex,Ai,Tasks,Annotators,Deployments,Event,Media,Observation,Occurence,Behavior,Grades
from database_site.models import *
import database_site.models
#from database_site.models_queryObjects import *
#from django_filters.rest_framework import DjangoFilterBackend
#from rest_framework import generics
#from rest_framework.serializers import *
from rest_framework import viewsets
#from rest_framework.views import APIView
from ..serializers import *
from ..Objects import *
#from .serializers import TaxonSerializer, AiSerializer,LifestageSerializer,SexSerializer,LocationSerializer,TasksSerializer,AnnotatorsSerializer,DeploymentsSerializer,MediaSerializer,ObservationSerializer,OccurenceSerializer,BehaviorSerializer,GradesSerializer,EventSerializer
#from rest_framework.decorators import api_view
#from django.http.response import JsonResponse
#from rest_framework.parsers import JSONParser
#from rest_framework import status
#import django_filters.rest_framework
#from rest_framework import filters
#import pandas as pd
#from django.core import serializers
from datetime import datetime, timedelta
import pytz
utc=pytz.UTC
#from io import StringIO, BytesIO
#import csv , zipfile
#from django.db.models import Q
#from django.core.files import File
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from database_site.functions import *
#import django.contrib.auth.models
import pandas as pd
from rest_framework import response


def GetEventDate(img_cluster):
    if hasattr(img_cluster.eventid, 'eventid'):
        return img_cluster.eventid.eventdate.replace(tzinfo=utc)
    return img_cluster.eventdate.replace(tzinfo=utc)

def Event4SupraEvent(img):
    if hasattr(img.eventid, 'eventid'):
        return img.eventid.eventid
    return img.eventid

def GroupBySupraEventID(df,time_interval):
    df['timestamp'] = df['timestamp'].str.split("+").str[0]
    df['interval'] = df["timestamp"].diff().apply(lambda x: x/np.timedelta64(1, 'm')).fillna(0).astype('int64')


def FilterData(requst_data):#start=None,end=None,animal=None,cameraid=None):
    """
    calculate supra event id for each picture in data
    Note - request_data = request.data: should have a legit cameraid, animal (generic name) and range date (start, end) in iso format.
    returns csv with queried data by the above parameters
    """

    ImgsQueryset = database_site.models.Image.objects.filter(cameraid = requst_data['cameraid']).select_related('eventid').filter(eventid__eventdate__range=[requst_data['start'],requst_data['end']])
    OccQueryset = Occurence.objects.filter(taxonid__genericname = requst_data['animal']).select_related('eventid')
    toReturn = {}
    for o in ImgsQueryset:
        queryset = OccQueryset.filter(eventid = o.eventid).last()
        if queryset:
            toReturn[queryset.eventid.eventid]=dict()
            toReturn[queryset.eventid.eventid]['filepath'] = database_site.models.Image.objects.get(eventid=queryset.eventid).filepath.path
            toReturn[queryset.eventid.eventid]['cameraid'] = database_site.models.Image.objects.get(eventid=queryset.eventid).cameraid
            toReturn[queryset.eventid.eventid]['animal'] = queryset.taxonid.genericname
            toReturn[queryset.eventid.eventid]['timestamp'] = queryset.eventid.eventdate

    res = pd.DataFrame(toReturn).T
    return res


class Zooniverse(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    """
    create data for zooniverse format using date range, species and camera
    """
    def list(self, request):
       # SupraEventDict,SupraEventData = CaulculateSupraEventID(request.data['start'], request.data['end'],request.data['animal'],request.data['cameraid'])
        res = FilterData(request.data)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=query_results.csv'  # alter as needed
        res.to_csv(response)  # with other applicable parameters
        return response









