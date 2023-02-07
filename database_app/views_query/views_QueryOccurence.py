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
from django.db.models import Subquery, OuterRef
from django.db.models import Case, When, Value, IntegerField, Q

def GetRelatedVideos(sequenceid,locationid,taxonid,cameraid,supraeventid):
    """ get videos related to frames (by sequenceid)"""

    vid = Video.objects.get(videoid = sequenceid)
    vid_event = {"event_datetime" : vid.eventdate, "inner_eventid" : None, "locationid" : locationid, "occurenceid" : None, "taxonid" : taxonid, "sequenceid" : sequenceid, "cameraid" : cameraid, "filepath" : vid.filepath.url, "eventid" : supraeventid}
    return vid_event

def CalcSupraEventID(events_dict,time_interval):
    """
    calculate supra-event-id by interval
    """
    time_interval = timedelta(minutes=time_interval)
    last_end, supraeventid, vids_seqs, vids_dict = 0, 0, [], []
    for event in events_dict:
        event_datetime = event['eventid__eventdate']
        if last_end == 0 or event_datetime - last_end > time_interval:
            supraeventid+=1
        
        event['supraeventid'] = supraeventid
        if "sequenceid" in event and event["sequenceid"] not in vids_seqs and event["sequenceid"] is not None: #add relevant videos
            vids_dict.append(GetRelatedVideos(event["sequenceid"], event['eventid__locationid'], event['taxonid_id'], event['cameraid'], supraeventid))
            vids_seqs.append(event["sequenceid"])
        last_end = event_datetime
    return events_dict, vids_dict

def Convert2csv(imgs_data, vids_data):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'
    writer = csv.writer(response)
    headers = ["event_datetime","inner_eventid","locationid", "occurenceid", "taxonid","sequenceid","cameraid","filepath", "eventid"]
    writer.writerow(headers)
    for item in imgs_data:
        writer.writerow(item.values())
    for item in vids_data:
        writer.writerow(item.values())
    return response


def FilterData(requst_data):
    """
    filter data by cameraid, start, end and taxonid (according to NCBI(
    """
    ImgsQueryset = database_site.models.Image.objects.filter(cameraid = requst_data['cameraid']).select_related('eventid').filter(eventid__eventdate__range=[requst_data['start'],requst_data['end']])
    seq_subquery = ImgsQueryset.filter(eventid=OuterRef('eventid')).values('sequenceid__sequenceid')[:1]
    cam_subquery = ImgsQueryset.filter(eventid=OuterRef('eventid')).values('cameraid')[:1]
    path_subquery = ImgsQueryset.filter(eventid=OuterRef('eventid')).values('filepath')[:1]
    OccQueryset = Occurrence.objects.filter(taxonid__taxonid = requst_data['taxonid']).select_related('eventid').filter(eventid__in = ImgsQueryset.values_list('eventid', flat=True)).order_by('eventid__eventdate').values('eventid__eventdate', 'eventid_id', 'eventid__locationid', 'occurrenceid', 'taxonid_id').annotate(sequenceid=Subquery(seq_subquery)).annotate(cameraid=Subquery(cam_subquery)).annotate(filepath=Subquery(path_subquery))

    return OccQueryset 

class Zooniverse(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    """
    create data for zooniverse format using date range, species and camera
    """
    def list(self, request):
        res =  FilterData(request.data)
        imgs,vids = CalcSupraEventID(res, request.data['interval'])
            
        response = Convert2csv(imgs,vids)
        return response










