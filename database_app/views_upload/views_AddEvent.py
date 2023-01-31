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
    data['sequenceid'] = Sequence.objects.get(sequenceid = data['sequenceid']) if 'sequenceid' in data else None
    newImage = Image(eventid = data['eventid'], filepath = data['filepath'], sequenceid = data['sequenceid'], cameraid = data['cameraid'])
    newImage.save()
    return newImage

def AddSequence(videoid, seq_type):
    newSequence = Sequence(sequenceid = videoid.videoid, sequencetype = seq_type)
    newSequence.save()
    return newSequence

def SaveNewVideo(data):
    data['eventRemarks'] = "" if 'eventRemarks' not in data else data['eventRemarks']
    newVideo = Video(filepath = data['filepath'],  eventdate = data['eventDate'], locationid = data['locationid'], samplingprotocol = data['samplingProtocol'], cameraid = data['cameraid'])#, eventRemarks = data['eventRemarks'])
    newVideo.save()
    return newVideo

def FindDeployment(data):
    try:
        #Deploy = Deployment.objects.filter(cameraid = data['cameraid']).filter(start__lte = data['date_time'].replace(tzinfo=utc)).filter(end__gte = data['date_time'].replace(tzinfo=utc)).last()
        Deploy = Deployment.objects.filter(cameraid = data['cameraid']).filter(start__lte = data['date_time']).filter(end__gte = data['date_time']).last()
    except:
        raise ValidationError("No Deployment for cameraID. please provide a locationid, or add camera deployment")
    return Deploy.locationid.locationid

def GetOccurrenceData(data):

    if not 'count' in data or data['count'] == 0:
        return None
    newOccurrences = []
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
        newOccrence = Occurrence(eventid = data['eventid'], taxonid = taxonid, behaviorid = behaviorid, sexid = sexid, lifestageid = lifestageid, individualcount = count)
        newOccrence.save()
        #newOccurrences.append(newOccurrence)
        return newOccrence
    


class AddNewImageWithExif(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    def create(self,request):
        #print (request.data)
        #print("Uploading Image With Exif")
        filepath = request.data['File']
        exif = GetImageExif(filepath)
        request.data['date_time'] = ValidateDateTime(exif)
        request.data['cameraid']= exif['BodySerialNumber'] if 'BodySerialNumber' in exif else None
        #print(request.data)
        if 'locationid' not in request.data:
            request.data['locationid'] = FindDeployment(request.data)
        data = ValidateData(request)
        #print(data)
        try:
            """add new Event"""
            eventid = SaveNewEvent(data)
            data['eventid'] = eventid
        except:
            #print("no new event")
            return Response({"fail": {"failed" : "failed"}})
        else:
            try:
                """add New Image"""
                imageid = SaveNewImage(data)
            except:
                #print("no new image")
                raise ValidationError()
                return Response({"fail": {"failed" : "failed"}})
            else:
                if imageid.sequenceid.sequenceid:
                    seq = imageid.sequenceid.sequenceid
                else:
                    seq = imageid.sequenceid
                request.data['eventid'] = eventid
                occureunceid = GetOccurrenceData(request.data)

        returnData = {'imageid' : imageid.imageid, 'eventid' : eventid.eventid, 'sequenceid' : seq,  'filepath' : imageid.filepath.path}
        return Response({"data" : returnData})
        #print(returnData)
        #except:
            #print ("no")
        #def update(self,request):


class AddNewOccurrence(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OccurrenceSerializer
    def create(self,request):
        Event_obj = Events.objects.get(eventid = data['eventid'])
        if len(Event_obj) == 0:
            raise ValidationError("no such event")
        occureunceid = GetOccurrenceData(request.data)

    
class UploadVideoWithExif(viewsets.ViewSet): 
    permission_classes = [permissions.IsAuthenticated]
    def create(self, request):
        if 'File' not in request.data: raise ValidationError("No file was uploaded")
        exif = {'DateTimeOriginal' : request.data['DateTimeOriginal']}
        #exif['DateTimeOriginal'] = GetVideoExif(request.data['file'])
        request.data['date_time'] = ValidateDateTime(exif)
        request.data['locationid'] = FindDeployment(request.data) if 'locationid' not in request.data else request.data['locationid']
        #request.data['cameraid']= exif['BodySerialNumber'] if 'BodySerialNumber' in exif else None
        data = ValidateData(request)
        videoid = SaveNewVideo(data)
        Sequence = AddSequence(videoid, "Video")
        if 'Sherable' in request.data and request.data['Sherable'] == 'True':
            print("converting")
            convertedFileName = ConvertVideo(videoid)
        else:
            print("no sherable")
        return Response({"sequenceid" : Sequence.sequenceid})








