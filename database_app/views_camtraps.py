from django.http import HttpResponse
from rest_framework.viewsets import ViewSet,ReadOnlyModelViewSet
#from django.shortcuts import render
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
utc=pytz.UTC
from io import StringIO, BytesIO
import csv , zipfile
from django.db.models import Q
from django.core.files import File
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from database_site.functions import * 
import django.contrib.auth.models

"""
class MultipleImage_VIEW(viewsets.ViewSet):
    def upload(self,request):
        images = request.FILES.getlist('images')
        for image in images:
            MultipleImage.objects.create(images=image)
        images = MultipleImage.objects.all()
        return Response({'queryset': images})
"""
IP = "http://127.0.0.1:8000/"
class Media_VIEW(viewsets.ViewSet):
    """
    create Media table for camtraps DP
    """
    permission_classes = [permissions.IsAuthenticated]
    def list(self, request):
        MediaData = []
        queryset = Event.objects.all()
        SupraEventDict,SupraEventData = CaulculateSupraEventID(request.data)
        print(SupraEventData)
        for e in queryset:
            if e.deploymentid != "None":
                fileName = (str(e.filepath).split("\\")[-1]).split("/")[-1]
                exif = GetImageExif(e.filepath)
                supraeventid = SupraEventDict[e.eventid]
                MediaData.append(MediaInfo(
                    mediaid=e.eventid,
                    deploymentid = e.deploymentid.deploymentid,
                    sequenceid=supraeventid,
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



def GetEventDate(img_cluster):
    if hasattr(img_cluster.eventid, 'eventid'):
        return img_cluster.eventid.eventdate.replace(tzinfo=utc)
    return img_cluster.eventdate.replace(tzinfo=utc)

def Event4SupraEvent(img):
    if hasattr(img.eventid, 'eventid'):
        return img.eventid.eventid
    return img.eventid



def CaulculateSupraEventID(request_data):#start=None,end=None,animal=None,cameraid=None):
    """
    calculate supra event id for each picture in data
    """
    Imgs_SupraEventDict = dict()
    SupraEventData = dict()
    imgs_cluster = GetImageCluster(request_data)#start,end,animal,cameraid)
    if len(imgs_cluster) > 0:
        SupraEventStart = GetEventDate(imgs_cluster[0])
        SupraEventEnd = GetEventDate(imgs_cluster[0]) + timedelta(minutes=15)
        SupraEventID = 0
        Bool = 0
        for img in imgs_cluster:
            if Bool == 0: #First supra event id
                Bool = 1
                SupraEventStart = GetEventDate(imgs_cluster[0])
                SupraEventEnd =  GetEventDate(imgs_cluster[0])
                SupraEventID = 1
                SupraEventData[SupraEventID] = dict()
                SupraEventData[SupraEventID]['images'] = list()
                SupraEventData[SupraEventID]['start'] = SupraEventStart
                SupraEventData[SupraEventID]['end'] = SupraEventStart
            else: #not first
                EventStart =  GetEventDate(img)
                if EventStart >= SupraEventEnd + timedelta(minutes=15): # a new supraeventid
                    SupraEventData[SupraEventID]['end'] = SupraEventEnd
                    SupraEventStart = EventStart
                    SupraEventEnd =  GetEventDate(img)
                    SupraEventID+=1 #increase super event id by one
                    SupraEventData[SupraEventID] = dict()
                    SupraEventData[SupraEventID]['start'] = SupraEventStart
                    SupraEventData[SupraEventID]['end'] = SupraEventStart
                    SupraEventData[SupraEventID]['images'] = list()
                else: #this is not the beginning of this super event id
                    SupraEventEnd = GetEventDate(img)
                    SupraEventData[SupraEventID]['end'] = SupraEventEnd
            Imgs_SupraEventDict[Event4SupraEvent(img)] = SupraEventID
            SupraEventData[SupraEventID]['images'].append(Event4SupraEvent(img))
    return Imgs_SupraEventDict, SupraEventData


def GetImageCluster(requst_data):#start=None,end=None,animal=None,cameraid=None):
    """
    get images that matches user's query
    """
    imgs_cluster = Occurence.objects.filter(taxonid__genericname = requst_data['animal']).filter(eventid__deploymentid__cameraid=requst_data['cameraid']).filter(eventid__eventdate__range=[requst_data['start'],requst_data['end']])
    
    return imgs_cluster


def ZooniVideo(SupraEventDict,SupraEventData,request):
    if len (SupraEventData) > 0:
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': f'attachment; filename="manifest_video.csv"'}
        )
        writer = csv.writer(response, quoting=csv.QUOTE_NONE, escapechar = ' ')
        all_filenames , videosData , header , max_videos = [], [], [], 0
        header.extend(["#subject_id","#mimeType","#mimeCount"])
        csvfile = open("manifest_video.csv","w")
        for SupraEventID in SupraEventData:
            Event_Videos = []
            SupraEventStart = SupraEventData[SupraEventID]['start']
            SupraEventEnd = SupraEventData[SupraEventID]['end']+timedelta(seconds=20)
            for EventID in set(SupraEventData[SupraEventID]['images']):
                SequenceID = Event.objects.get(eventid=EventID).sequenceid
                VideoID = SequenceID.videoid
                SharedVideoID = SharedVideo.objects.get(videoid = VideoID)  
                videoURL = IP+"media/"+str(VideoID.filepath)
                #print(str(VideoID.filepath))
                SharedPath = (str(VideoID.filepath)).replace("videos","videos_to_share")+".ogg"
                
                SharedvideoURL = IP+"media/"+str(SharedVideoID.filepath)
               # if settings.MEDIA_ROOT+"/"+str(VideoID.filepath) not in all_filenames:
               # if settings.MEDIA_ROOT+"/"+str(SharedVideoID.filepath) not in all_filenames:
                if settings.MEDIA_ROOT+"/"+str(SharedPath) not in all_filenames:
                    #all_filenames.append(settings.MEDIA_ROOT+"/"+str(SharedVideoID.filepath))
                    all_filenames.append(settings.MEDIA_ROOT+"/"+SharedPath)
                    #Event_Videos.append((str(SharedVideoID.filepath).split("\\")[-1]).split("/")[-1]) 
                    Event_Videos.append(os.path.basename(SharedPath))
            try:
                LocationName = Event.objects.get(eventid = SupraEventData[SupraEventID]['images'][0]).deploymentid.locationid.locationname
            except:
                LocationName = Event.objects.get(eventid = SupraEventData[SupraEventID]['images'][0]).locationid.locationname
            if len(Event_Videos) > 0:
                videosData.append(ImgInfo(
                    start = SupraEventStart,
                    end = SupraEventEnd,
                    cameraid = request.data['cameraid'],
                    animal = request.data['animal'],
                    imgName = Event_Videos,
                    imgType='video/ogg',
                    supraeventid = SupraEventID,
                    locationName = LocationName
                ).__dict__)
            if len(Event_Videos) > max_videos:
                max_videos = len(Event_Videos)
        zip_subdir = LocationName+"_Vids"
        zip_filename = "%s.zip" % zip_subdir
        s = BytesIO()
        zf = zipfile.ZipFile(s, "w")
        for fpath in all_filenames:
            fdir, fname = os.path.split(fpath)
            zip_path = os.path.join(zip_subdir, fname)
            zf.write(fpath, zip_path)
        for i in range(max_videos):
            header.append("#video"+str(i+1))
        HeaderString = "Date,Start,End,Duration,Location"
        header.append(HeaderString)
        writer.writerow(header)
        csvfile.write(",".join(header)+"\n")
        for videoData in videosData:
            from_hour = videoData['start'].time()
            to_hour = videoData['end'].time()
            NumVideos = len(videoData['imgName'])
            writer.writerow([videoData['supraeventid'],videoData['imgType'],NumVideos,",".join(videoData['imgName'])+","*(max_videos-len(videoData['imgName'])),videoData['start'].date(),from_hour,to_hour,videoData['end']-videoData['start'],videoData['locationName']])
            csvfile.write(str(videoData['supraeventid'])+","+videoData['imgType']+","+str(NumVideos)+","+",".join(videoData['imgName'])+","*(max_videos-len(videoData['imgName']))+","+str(videoData['start'].date())+","+str(from_hour)+","+str(to_hour)+","+str(videoData['end']-videoData['start'])+","+str(videoData['locationName'])+"\n")
        csvfile.close()
        fdir, fname = os.path.split('manifest_video.csv')
        zip_path = os.path.join(zip_subdir, fname)
        zf.write('manifest_video.csv', zip_path)
        zf.close()
        resp = HttpResponse(s.getvalue(),  content_type = "application/x-zip-compressed" )
        resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
        return resp
    return Response({'queryset': {'none':'none'}})


import sys

class Zooniverse(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    """
    create data for zooniverse format using date range, species and camera
    """
    def create(self, request):
       # SupraEventDict,SupraEventData = CaulculateSupraEventID(request.data['start'], request.data['end'],request.data['animal'],request.data['cameraid'])
        SupraEventDict,SupraEventData = CaulculateSupraEventID(request.data)        
        if request.data['VIDEO'] == "True":
           resp = ZooniVideo(SupraEventDict,SupraEventData,request)
           return resp
        print(len(SupraEventData))
        if len(SupraEventData) > 0:
            camera=request.data['cameraid']
            response = HttpResponse(
                    content_type='text/csv',
                    headers={'Content-Disposition': f'attachment; filename="manifest.csv"'}
            )
            #csvfile = open("manifest.csv","w")
            writer = csv.writer(response, quoting=csv.QUOTE_NONE, escapechar = ' ')
            all_filenames , imgsData , header , max_images = [], [], [], 0
            header.extend(["#subject_id","#mimeType","#mimeCount"])
            csvfile = open("manifest.csv","w")
            for SupraEventID in SupraEventData:
                Event_Imgs = []
                SupraEventStart = SupraEventData[SupraEventID]['start']
                SupraEventEnd = SupraEventData[SupraEventID]['end']
                for EventID in set(SupraEventData[SupraEventID]['images']):
                    imgURL = IP+"media/"+str(Event.objects.get(eventid=EventID).filepath)
                    if settings.MEDIA_ROOT+"/"+str(Event.objects.get(eventid=EventID).filepath) not in all_filenames:
                        all_filenames.append(settings.MEDIA_ROOT+"/"+str(Event.objects.get(eventid=EventID).filepath))
                        Event_Imgs.append(os.path.basename(str(Event.objects.get(eventid=EventID).filepath)))
                    #print(str(Event.objects.get(eventid=EventID).filepath).split("\\")[-1])
                try:
                    LocationName = Event.objects.get(eventid = SupraEventData[SupraEventID]['images'][0]).deploymentid.locationid.locationname
                except:
                    LocationName = Event.objects.get(eventid = SupraEventData[SupraEventID]['images'][0]).locationid.locationname
                if len(Event_Imgs) > 0:
                    imgsData.append(ImgInfo(
                        start = SupraEventStart,
                        end = SupraEventEnd,
                        cameraid = request.data['cameraid'],
                        animal = request.data['animal'],
                        imgName = Event_Imgs,
                        imgType='image/jpeg',
                        supraeventid = SupraEventID,
                        locationName = LocationName
                    ).__dict__)
                if len(Event_Imgs) > max_images:
                    max_images = len(Event_Imgs)
            zip_subdir = LocationName+"_Imgs"
            zip_filename = "%s.zip" % zip_subdir
            s = BytesIO()
            zf = zipfile.ZipFile(s, "w")
            for fpath in all_filenames:
                
                #print(fpath)
                #fpath.filepath = fpath.replace(".jpg",".jpeg")
                #fpath.filepath = fpath.replace(".JPG",".JPEG")
                fdir, fname = os.path.split(fpath)
                zip_path = os.path.join(zip_subdir, fname)
                zf.write(fpath, zip_path)

            for i in range(max_images):
                header.append("#image"+str(i+1))
            HeaderString = "Date,Start,End,Duration,Location"
            header.append(HeaderString)
            writer.writerow(header)
            csvfile.write(",".join(header)+"\n")
            for imgData in imgsData:
                from_hour = imgData['start'].time()
                to_hour = imgData['end'].time()
                NumImages = len(imgData['imgName'])
                imgData['imgName'] = [i.replace(".jpg",".jpeg") for i in imgData['imgName']]
                imgData['imgName'] = [i.replace(".JPG",".JPEG") for i in imgData['imgName']]
                #print(imgData['imgName'])
                writer.writerow([imgData['supraeventid'],imgData['imgType'],NumImages,",".join(imgData['imgName'])+","*(max_images-len(imgData['imgName'])),imgData['start'].date(),from_hour,to_hour,imgData['end']-imgData['start']+timedelta(seconds=20),imgData['locationName']])
                csvfile.write(str(imgData['supraeventid'])+","+imgData['imgType']+","+str(NumImages)+","+",".join(imgData['imgName'])+","*(max_images-len(imgData['imgName']))+","+str(imgData['start'].date())+","+str(from_hour)+","+str(to_hour)+","+str(imgData['end']-imgData['start']+timedelta(seconds=20))+","+str(imgData['locationName'])+"\n")
            csvfile.close()
            fdir, fname = os.path.split('manifest.csv')
            zip_path = os.path.join(zip_subdir, fname)
            zf.write('manifest.csv', zip_path)
            zf.close()
            
            resp = HttpResponse(s.getvalue(),  content_type = "application/x-zip-compressed" )
            resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
            return resp
        return Response({'queryset': {'none':'none'}})











