# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


from django.dispatch import receiver
from django.db.models.signals import post_save
from datetime import datetime, timedelta, date
from .models_AUTH_PERMISSIONS import *
from .models_helpTables import *
from .models_camtraps import *
import pytz
utc=pytz.UTC
from django.utils.deconstruct import deconstructible
from PIL import Image
import PIL.ExifTags


@deconstructible
class PathAndRename(object):
    def __init__(self, sub_path):
        self.path = sub_path
    
    def __call__(self, instance, filename):
        Loc = instance.deploymentid.locationid.locationid
        camera_id = instance.deploymentid.cameraid
        filename = str(instance.eventdate)+"_"+filename
        today = str(date.today())
        filepath = os.path.join(path,camera_id,Loc,today,filename)
        return filepath

path_and_rename = PathAndRename("/images")



class Event(models.Model):
    samplingprotocol = models.CharField(db_column='samplingProtocol', max_length=255)  # Field name made lowercase.
    eventdate = models.DateTimeField(db_column='eventDate', blank=True, null=True, editable = False)  # Field name made lowercase.
    eventremarks = models.CharField(db_column='eventRemarks', max_length=255, blank=True, null=True)  # Field name made lowercase.
    supraeventid = models.IntegerField(db_column='supraEventID', blank=True, null=True, editable = False)  # Field name made lowercase.
    deploymentid= models.ForeignKey('Deployments', db_column = 'deploymentID', on_delete=models.CASCADE, editable = False)
    filepath = models.ImageField(upload_to=path_and_rename)
    eventid = models.AutoField(db_column = "eventID", primary_key=True, editable = False)
    
    class Meta:
        managed = False
        db_table = 'Event'

    def save(self, *args, **kwargs):
        #raise ValidationError(self.filepath.path)
        image = Image.open(self.filepath)
        exif_data = image._getexif()
        exif = {
            PIL.ExifTags.TAGS[k]: v
                for k, v in image._getexif().items()
                    if k in PIL.ExifTags.TAGS
        }
        cameraid = exif['BodySerialNumber']
        try:
            date_object = datetime.strptime(exif['DateTimeOriginal'],'%Y:%m:%d %H:%M:%S' )
            timestamp = date_object
        except:
            raise ValidationError("no date in exif data or datetime is in a wrong format")
        camera_deployments = Deployments.objects.filter(cameraid = cameraid)
        try:
            camera_deployments = Deployments.objects.filter(cameraid = cameraid)
            for deployment in camera_deployments:
                start_time =  deployment.start.replace(tzinfo=utc)
                end_time =  deployment.end.replace(tzinfo=utc)
                curr_time = date_object.replace(tzinfo=utc)
                if start_time <= curr_time and end_time >= curr_time:
                    deploymentid = deployment
                    break
            if not deploymentid:
                raise ValidationError("deployment is wrong " + cameraid+ "  " + str(date_object))
        except:
            raise ValidationError("deployment is wrong " + cameraid+ "  " + str(date_object))
        mediaid =  str(timestamp)+str(self.filepath)
        LastSupraEventID = Event.objects.all().order_by('supraeventid').last() # Get lase supraeventid
        try:
            LastTime = Event.objects.filter(deploymentid = deploymentid).order_by('-eventdate')[0] # previous image of this camera and location (deployment)
        except:  # this is the first image of this camera and location
            LastTime = timestamp - timedelta(minutes=16) #last time = this time -16m, then supraeventid will be increased by 1 (a new supraeventid will be assigned to this image
        else:
            LastTime = (LastTime.eventdate).replace(tzinfo=utc) # last datetime of this camera and location (deployment)
        ThisTime = timestamp.replace(tzinfo=utc) #this datetime of this camera and location (deployment)
        DeltaTime = (LastTime + timedelta(minutes=15)).replace(tzinfo=utc)
        if not LastSupraEventID: # this is the first image (of all cameras and locations (deployments)
            SupraEventID=1
        elif DeltaTime <= ThisTime: # this is a new supraeventid
            SupraEventID = int(LastSupraEventID.supraeventid)+1
        else: #this is the same supraeventid
            SupraEventID = int(LastSupraEventID.supraeventid)
        samplingprotocol = 'motion detecttion'

        self.samplingprotocol = samplingprotocol
        self.eventdate = timestamp
        self.eventremarks = self.eventremarks
        self.deploymentid = deploymentid
        self.supraeventid = SupraEventID
        super(Event, self).save()

    class Meta:
        managed = False
        db_table = 'Event'




class Occurence(models.Model):
    eventid = models.ForeignKey('Event', on_delete = models.CASCADE, db_column='eventID')  # Field name made lowercase.
    taxonid = models.ForeignKey('Taxon', db_column='taxonID', on_delete=models.CASCADE)  # Field name made lowercase.
    individualcount = models.IntegerField(db_column='individualCount')  # Field name made lowercase.
    sexid = models.ForeignKey('Sex', on_delete=models.CASCADE, db_column='sexID')  # Field name made lowercase.
    lifestageid = models.ForeignKey('Lifestage', on_delete=models.CASCADE, db_column='lifeStageID')  # Field name made lowercase.
    behaviorid = models.ForeignKey('Behavior', on_delete=models.CASCADE, db_column='behaviorID')  # Field name made lowercase.
    occurenceid = models.AutoField(db_column = "occurenceID", primary_key=True, editable = False)

    class Meta:
        managed = False
        db_table = 'Occurence'
        constraints = [
            models.UniqueConstraint(
            fields=['eventid', 'occurenceid'], name='unique_event_occurence_combination'
            )
        ]



class Grades(models.Model):
    annotatorid = models.ForeignKey(Annotators, on_delete = models.CASCADE, db_column='annotatorid')  # Field name made lowercase.
    taskid = models.ForeignKey('Tasks', on_delete = models.CASCADE, db_column='taskid')  # Field name made lowercase.
    eventid = models.ForeignKey('Occurence', on_delete = models.CASCADE, db_column='eventID', related_name='Occurence_eventid')  # Field name made lowercase.
    occurenceid = models.ForeignKey('Occurence', on_delete = models.CASCADE, db_column='occurenceID', related_name = 'Occurence_occurenceid')  # Field name made lowercase.
    grade = models.FloatField()
    field_id = models.AutoField(db_column='_id', primary_key = True,editable = False)

    class Meta:
        managed = False
        db_table = 'Grades'
        unique_together = (('eventid', 'occurenceid', 'taskid', 'annotatorid'),)
                                                                



@receiver(pre_save, sender = Event)
def VerifyChronologicalUploading(sender, instance, **kwarg):
    try:
        LastUploadTime = sender.objects.filter(deploymentid = instance.deploymentid).order_by('eventdate').last()
    except:
        pass
    else:
        if LastUploadTime:
            LastUploadTime = LastUploadTime.eventdate.replace(tzinfo=utc)
            time = instance.eventdate.replace(tzinfo=utc)
            if LastUploadTime >= time:
                raise ValidationError("New upload was taken earlier than latest upload")




"""
@receiver(signal=post_save, sender=Observation, dispatch_uid='add_occurence_on_new_observation')
def CreateOccurenceFromObservation(sender, instance, **kwargs):
    new_occurence = Occurence(
        occurenceid = instance.observationid,
        eventid = Event.objects.get(eventid = instance.mediaid),
        taxonid = instance.taxonid,
        sexid = Sex.objects.get(sextype = instance.sex),
        lifestageid = Lifestage.objects.get(lifestagetype = instance.lifestage),
        behaviorid = Behavior.objects.get(behaviortype = instance.behavior),
        individualcount = instance.count

    )
    new_occurence.save()
"""


