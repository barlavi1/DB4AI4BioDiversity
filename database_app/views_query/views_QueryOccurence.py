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

def CalcSupraEventID(events_dict,time_interval):

    res = sorted(events_dict.items(), key = lambda x: x[1]['timestamp'])
    supraeventid, last_end, supraeventDict, NumImagesDict = 0,0,{}, {}
    time_interval = timedelta(minutes=time_interval)
    for res_event in res:
        res_datetime = res_event[1]['timestamp']
        if last_end == 0 or res_datetime - last_end > time_interval:
            supraeventid+=1
            NumImagesDict[supraeventid] = {}
            NumImagesDict[supraeventid]['events'] = list()
            NumImagesDict[supraeventid]['num'] = 0
            NumImagesDict[supraeventid]['start'] = res_event[1]['timestamp']
            NumImagesDict[supraeventid]['end'] = res_event[1]['timestamp']
            NumImagesDict[supraeventid]['location'] = res_event[1]['location']
            NumImagesDict[supraeventid]['camera'] = res_event[1]['cameraid']
            if  'sequenceid' in res_event[1]:
                 NumImagesDict[supraeventid]['videos'] = list()

        NumImagesDict[supraeventid]['events'].append(res_event[1]['filepath'])
        NumImagesDict[supraeventid]['num']+=1
        NumImagesDict[supraeventid]['end'] = res_event[1]['timestamp']
        if 'sequenceid' in res_event[1]:
            videofile = Video.objects.get(videoid = res_event[1]['sequenceid']).filepath.url
            NumImagesDict[supraeventid]['videos'].append(videofile)
        last_end = res_datetime
    return NumImagesDict


def GenerateManifest(res,filetype):
    if filetype == "videos":
        mime_type = "video/mp4"
        maxEvents = max(len(list(set(res[supraEvent]['videos']))) for supraEvent in res)
        csv_headers = ["#subject_id","#mime_Type","mimeCount"]+["#video"+str(i+1) for i in range(maxEvents)] + ["Date","Start","End","Duration","Location","Camera"]
    else:
        maxEvents = max(int(res[inner]['num']) for inner in res)
        mime_type = "image/jpeg"
        csv_headers = ["#subject_id","#mime_Type","mimeCount"]+["#image"+str(i+1) for i in range(maxEvents)] + ["Date","Start","End","Duration","Location","Camera"]
    buffer = io.StringIO()
    wr = csv.writer(buffer)
    wr.writerow(csv_headers)
    for supraEvent in res:
        SupraEvents = res[supraEvent]
        start = res[supraEvent]['start']
        date = start.date()
        end = res[supraEvent]['end']
        if filetype == "videos":
            filepaths = list(set(res[supraEvent]['videos']))
            filepaths = sorted(filepaths)
            [filepaths.append("") for i in range(maxEvents-len(list(set(res[supraEvent]['videos']))))]
            count = len(list(set(res[supraEvent]['videos'])))
        else:
            filepaths = res[supraEvent]['events']
            [filepaths.append("") for i in range(maxEvents-len(res[supraEvent]['events']))]
            count = res[supraEvent]['num']
        #print(filepaths)

        duration = end - start
        location = res[supraEvent]['location']
        camera = res[supraEvent]['camera']
        #count = res[supraEvent]['num']
        outline = [supraEvent,mime_type,count]+filepaths+[date,start,end,duration,location,camera]
        wr.writerow(outline)
    buffer.seek(0)
    wr = csv.writer(buffer)
    response = HttpResponse(buffer, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="zooniverse_response.csv"'
    return (response)
        



def FilterData(requst_data):
    """
    calculate supra event id for each picture in data
    Note - request_data = request.data: should have a legit cameraid, animal (generic name) and range date (start, end) in iso format.
    returns csv with queried data by the above parameters
    """

    ImgsQueryset = database_site.models.Image.objects.filter(cameraid = requst_data['cameraid']).select_related('eventid').filter(eventid__eventdate__range=[requst_data['start'],requst_data['end']])
    OccQueryset = Occurrence.objects.filter(taxonid__genericname = requst_data['animal']).select_related('eventid').filter(eventid__in = ImgsQueryset.values_list('eventid', flat=True))
    toReturn = {}
    for queryset in OccQueryset:
        if 1 == 1:
            toReturn[queryset.eventid.eventid]=dict()
            toReturn[queryset.eventid.eventid]['eventid'] = queryset.eventid.eventid
            toReturn[queryset.eventid.eventid]['filepath'] = database_site.models.Image.objects.get(eventid=queryset.eventid).filepath.url
            toReturn[queryset.eventid.eventid]['cameraid'] = database_site.models.Image.objects.get(eventid=queryset.eventid).cameraid
            toReturn[queryset.eventid.eventid]['animal'] = queryset.taxonid.genericname
            toReturn[queryset.eventid.eventid]['timestamp'] = queryset.eventid.eventdate
            toReturn[queryset.eventid.eventid]['occurenceid'] = queryset.occurenceid
            toReturn[queryset.eventid.eventid]['location'] = queryset.eventid.locationid.locationname
            try:
                toReturn[queryset.eventid.eventid]['sequenceid'] =  database_site.models.Image.objects.get(eventid=queryset.eventid).sequenceid.sequenceid
            except:
                print("no such sequenceid")
            
    return toReturn


class Zooniverse(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    """
    create data for zooniverse format using date range, species and camera
    """
    def list(self, request):
        res = FilterData(request.data)
        EventsInSupraEvent = CalcSupraEventID(res, request.data['interval'])
        if request.data['type'] == "videos":
            response = GenerateManifest(EventsInSupraEvent,"videos")
        else:
            response = GenerateManifest(EventsInSupraEvent,"images")
        return response









