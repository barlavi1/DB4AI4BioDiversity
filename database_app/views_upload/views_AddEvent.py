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
    """ saves new image with or without sequenceid """
    if 'sequenceid' in data: #frame from video
        newImage = Image(eventid = data['eventid'], filepath = data['filepath'], sequenceid = data['sequenceid'],cameraid = data['cameraid'])
        newImage.save()
        
        return newImage

    newImage = Image(eventid = data['eventid'], filepath = data['filepath'], cameraid = data['cameraid'])
    newImage.save()
    return newImage

def AddSequence(videoid, seq_type):
    """ save new sequence for every new saves video  """
    newSequence = Sequence(sequenceid = videoid.videoid, sequencetype = seq_type)
    newSequence.save()
    return newSequence

def SaveNewVideo(data):
    newVideo = Video(filepath = data['filepath'],  eventdate = data['eventDate'], locationid = data['locationid'], samplingprotocol = data['samplingProtocol'], cameraid = data['cameraid'])
    newVideo.save()
    return newVideo

def FindDeployment(data):
    """ find camera's deployment based on date range and camera id """
    try:
        Deploy = Deployment.objects.filter(cameraid = data['cameraid']).filter(start__lte = data['date_time']).filter(end__gte = data['date_time']).last()
    except:
        raise ValidationError("No Deployment for this cameraID within the provided dates. add deployment for this camera and date range")
    else:
        return Deploy.locationid.locationid

def Validate(data, arg):
    """ check if certain argument is in request """
    if arg not in data:
        raise ValidationError(f"{arg} must be provided")

def GetOccurrenceData(data):
    """ organize occurrence data """
    print("################################# in occurrence #########################")
    if 'count' not in data or data['count'] == 0: #no occurence was provided
        print("no occurrence")
        return None
    #newOccurrences = []
    count = data['count']
    taxon = data['taxon'] if 'taxon' in data else 0 #unknown
    behavior = data['behavior'] if 'behavior' in data else 0 #unknown
    lifestage = data['lifestage'] if 'lifestage' in data else 0 #unknown
    sex = data['sex'] if 'sex' in data else 0 #unknown
    i=0
    if True:
        try:
            taxonid = Taxon.objects.get(taxonid = taxon)
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise ValidationError(f"no such taxon id:  {taxon}")
        try:
            behaviorid = Behavior.objects.get(behavioid = behavior)
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise ValidationError(f"no such behaviorid: {behavior}")

        try:
            lifestageid = Lifestage.objects.get(lifestageid = lifestage)
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise ValidationError(f"no such lifestageid: {lifestage}")
        try:
            sexid = Sex.objects.get(sexid = sex)
        except:
            raise ValidationError(f"no such sexid: {sex}")
        newOccrence = Occurrence(eventid = data['eventid'], taxonid = taxonid, behaviorid = behaviorid, sexid = sexid, lifestageid = lifestageid, individualcount = count)
        newOccrence.save()
        return newOccrence
    

class AddNewImageWithExif(viewsets.ViewSet):
    """ Add new image - exif or request must contain a valid datetime stamp and cameraid """
    permission_classes = [permissions.IsAuthenticated]
    def create(self,request):
        
        ########## validate data is correct ######
        Validate(request.data, 'File')
        print("validated")
        filepath = request.data['File']
        if 'cameraid' not in request.data:
            
            exif = GetImageExif(filepath)
            print(exif)
            request.data['cameraid']= exif['BodySerialNumber'] if 'BodySerialNumber' in exif else None
            if request.data['cameraid'] == None:
                raise ValidationError(f"cameraid must be embedded in exif")
        
        exif['DateTimeOriginal'] = request.data[date_time] if 'date_time' in request.data else exif['DateTimeOriginal']
        request.data['date_time'] = ValidateDateTime(exif) #validate datetime is in exif and in the correct format
        request.data['locationid'] = FindDeployment(request.data) if not 'locationid' in request.data else request.data['locationid']
        if 'sequenceid' in request.data: #image is a frame from sequence (video or burst)
            try:
                data['sequenceid'] = Sequence.objects.get(sequenceid = request.data['sequenceid'])
            except:
                raise ValidationError(f"no such sequenceid: {data['sequenceid']}")
        data = GetData(request) #get data in organaized format
        
        ######## save new data to DB ######

        data['eiventid'] = SaveNewEvent(data) #add new event
        imageid = SaveNewImage(data) #add new image
        request.data['eventid'] = data['eventid']
        occureunceid = GetOccurrenceData(request.data) #add nenw occurrence
        returnData = {'imageid' : imageid.imageid, 'eventid' :  data['eventid'].eventid, 'filepath' : imageid.filepath.path}
        return Response(returnData)


class AddNewOccurrence(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OccurrenceSerializer
    def create(self,request):
        try:
            Event_obj = Events.objects.get(eventid = data['eventid'])
        except:
            raise ValidationError("no such event")
        occureunceid = GetOccurrenceData(request.data)

def GetVideoDateTime(video):
    ti_m = os.path.getmtime(video)
    datetimeObj = datetime.datetime.fromtimestamp(ti_m)
    return datetimeObj.isoformat().replace("T"," ")

class UploadVideoWithExif(viewsets.ViewSet): 
    permission_classes = [permissions.IsAuthenticated]
    def create(self, request):
        Validate(request.data, 'File')
        print("file is validated")
        if 'cameraid' not in request.data:
            raise ValidationError(f"cameraid must be provided")
        #exif = {'DateTimeOriginal' : request.data['DateTimeOriginal']}
        exif = {'DateTimeOriginal' : GetVideoExif(request.data['File'])} #insert datetime to exif
        #print(exif)
        #exif['DateTimeOriginal'] = GetVideoExif(request.data['file'])
        request.data['date_time'] = ValidateDateTime(exif)
        request.data['locationid'] = FindDeployment(request.data) if 'locationid' not in request.data else request.data['locationid']
        data = GetData(request)
        videoid = SaveNewVideo(data) # add new video
        Sequence = AddSequence(videoid, "Video") #add new sequence
        if 'Sherable' in request.data and request.data['Sherable'] == 'True':
            convertedFileName = ConvertVideo(videoid)
        return Response({"sequenceid" : Sequence.sequenceid})








