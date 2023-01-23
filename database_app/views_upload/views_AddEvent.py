from database_site.models import *
#from database_site.functions import *
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
import sys
import pytz
utc=pytz.UTC
from rest_framework.response import Response
from ..serializers import *

def SaveNewEvent(data):
    newEvent = Event(samplingprotocol = data['samplingProtocol'], eventdate = data['eventDate'], eventremarks = data['eventRemarks'], locationid = data['locationid'])
    newEvent.save()
    return newEvent

def SaveNewImage(data):
    newImage = Image(eventid = data['eventid'], filepath = data['filepath'], sequenceid = data['sequenceid'], cameraid = data['cameraid'])
    newImage.save()
    return newImage

def AddSequence(videoid, seq_type):
    newSequence = Sequence(sequenceid = videoid, sequencetype = seq_type)
    newSequence.save()
    return newSequence

def SaveNewVideo(data):
    newVideo = Video(filepath = data['filepath'],  eventdate = data['eventDate'], locationid = data['locationid'], samplingprotocol = data['samplingProtocol'], cameraid = data['cameraid'], eventRemarks = data['eventRemarks'])
    newVideo.save()
    return newVideo

def FindDeployment(data):
    try:
        #Deploy = Deployments.objects.filter(cameraid = data['cameraid']).filter(start__lte = data['date_time'].replace(tzinfo=utc)).filter(end__gte = data['date_time'].replace(tzinfo=utc)).last()
        Deploy = Deployments.objects.filter(cameraid = data['cameraid']).filter(start__lte = data['date_time']).filter(end__gte = data['date_time']).last()
    except:
        raise ValidationError("No Deployment for cameraID. please provide a locationid, or add camera deployment")
    return Deploy.locationid.locationid

def GetOccurenceData(data):

    if not 'count' in data or data['count'] == 0:
        return None
    newOccurences = []
    count = data['count']
    taxon = data['taxon'] if 'taxon' in data else "unknown"
    behavior = data['behavior'] if 'behavior' in data else "unknown"
    lifestage = data['lifestage'] if 'lifestage' in data else "unknown"
    sex = data['sex'] if 'sex' in data else "unknown"
    i=0
    if 1 == 1: 
        try:
            taxonid = Taxon.objects.get(genericname = taxon)
        except:
            raise ValidationError("no such taxon ", taxon)
        try:
            behaviorid = Behavior.objects.get(behaviortype = behavior)
        except:
            raise ValidationError("no such behavior")

        try:
            lifestageid = Lifestage.objects.get(lifestagetype = lifestage)
        except:
            raise ValidationError("no such lifestage")
        try:
            sexid = Sex.objects.get(sextype = sex)
        except:
            raise ValidationError("no such sex")
        newOccrence = Occurence(eventid = data['eventid'], taxonid = taxonid, behaviorid = behaviorid, sexid = sexid, lifestageid = lifestageid, individualcount = count)
        newOccrence.save()
        #newOccurences.append(newOccurence)
        return newOccrence
    


class AddNewImageWithExif(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    def create(self,request):
        #print (request.data)
        print("Uploading Image With Exif")
        filepath = request.data['File']
        exif = GetImageExif(filepath)
        request.data['date_time'] = ValidateDateTime(exif)
        request.data['cameraid']= exif['BodySerialNumber'] if 'BodySerialNumber' in exif else None
        print(request.data)
        if 'locationid' not in request.data:
            request.data['locationid'] = FindDeployment(request.data)
        data = ValidateData(request)
        #print(data)
        try:
            """add new Event"""
            eventid = SaveNewEvent(data)
            """add New Image"""
            data['eventid'] = eventid
            imageid = SaveNewImage(data)
            if imageid.sequenceid:
                seq = imageid.sequenceid.sequenceid
            else:
                seq = imageid.sequenceid
            request.data['eventid'] = eventid
        except:
            print("no")
            return Response({"fail": {"failed" : "failed"}})
        occureunceid = GetOccurenceData(request.data)

        returnData = {'imageid' : imageid.imageid, 'eventid' : eventid.eventid, 'sequenceid' : seq,  'filepath' : imageid.filepath.path}
        return Response(returnData)
        #print(returnData)
        #except:
            #print ("no")
        #def update(self,request):


class AddNewOccurence(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OccurenceSerializer
    def create(self,request):
        Event_obj = Events.objects.get(eventid = data['eventid'])
        if len(Event_obj) == 0:
            raise ValidationError("no such event")
        occureunceid = GetOccurenceData(request.data)

#class AddNewImageWithDate(viewsets.ViewSet):
#    permission_classes = [permissions.IsAuthenticated]
#    def create(self, request):
#        #data must contain Valid: 1.'file',  2.'location_id', 3.'date_time'
#        data = ValidateData(request)  #{filepath = 'samplingProtocol': samplingProtocol, 'eventRemarks' : eventRemarks, 'locationid' : locationid, 'sequenceid' : sequnece, 'cameraid' : cameraid}        
#        data['eventid'] = SaveNewEvent(data)
#        newImage = SaveNewImage(data)
       
#class UploadVideoWithData(viewsets.ViewSet):
#    permission_classes = [permissions.IsAuthenticated]
#    def create(self, request):
        #request.data['cameraid']= exif['BodySerialNumber'] if 'BodySerialNumber' in exif else None
#        data = ValidateData(request)
#        videoid = SaveNewVideo(data)
#        Sequence = AddSequence(videoid, "Video")

#        if 'Sharable' in request.data and request.data['Sharable'] == True:
#            ConvertVideo(videoid)
    
class UploadVideoWithExif(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    def create(self, request):
        if 'file' not in request.data: raise ValidationError("No file was uploaded")
        exif = {}
        exif['DateTimeOriginal'] = GetVideoExif(filepath)
        request.data['date_time'] = ValidateDateTime(exif)
        #request.data['cameraid']= exif['BodySerialNumber'] if 'BodySerialNumber' in exif else None
        data = ValidateData(request)
        videoid = SaveNewVideo(data)
        Sequence = AddSequence(videoid, "Video")

        if 'Sharable' in request.data and request.data['Sharable'] == True:
            ConvertVideo(videoid)







