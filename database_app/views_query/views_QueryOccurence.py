from django.http import HttpResponse
from rest_framework.viewsets import ViewSet
from database_site.models import *
import database_site.models
from rest_framework import viewsets
from ..serializers import *
from ..Objects import *
from datetime import datetime, timedelta
import pytz
utc=pytz.UTC
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from database_site.functions import *
import pandas as pd
from rest_framework import response
import io, csv

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
    #filter(eventid__in=[list of occurences ids])
    toReturn = {}
    for o in ImgsQueryset:
        #queryset = OccQueryset.filter(eventid = o.eventid).last()
        querysets = OccQueryset.filter(eventid = o.eventid)
        for queryset in querysets:
        #if queryset:
            toReturn[queryset.eventid.eventid]=dict()
            toReturn[queryset.eventid.eventid]['filepath'] = database_site.models.Image.objects.get(eventid=queryset.eventid).filepath.path
            toReturn[queryset.eventid.eventid]['cameraid'] = database_site.models.Image.objects.get(eventid=queryset.eventid).cameraid
            toReturn[queryset.eventid.eventid]['animal'] = queryset.taxonid.genericname
            toReturn[queryset.eventid.eventid]['timestamp'] = queryset.eventid.eventdate
            toReturn[queryset.eventid.eventid]['occurenceid'] = queryset.occurenceid

    #res = pd.DataFrame(toReturn).T
    return toReturn


class Zooniverse(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    """
    create data for zooniverse format using date range, species and camera
    """
    def list(self, request):
        res = FilterData(request.data)
       
        buffer = io.StringIO()
        wr = csv.writer(buffer)

        csv_headers = list(res[list(res.keys())[0]].keys())
        wr.writerow(csv_headers)
        for eventid in res:
            #cur_row = res[eventid]
            #outrow = res[eventid].values()
            wr.writerow(res[eventid].values())
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="query_response.csv"'
        return response









