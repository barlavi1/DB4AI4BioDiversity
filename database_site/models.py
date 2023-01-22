# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

#from embed_video.fields import EmbedVideoField

#from django.dispatch import receiver
#from django.db.models.signals import post_save
#from datetime import datetime, timedelta, date
from .models_AUTH_PERMISSIONS import *
from .models_helpTables import *
from .models_camtraps import *
import pytz
utc=pytz.UTC
from django.utils.deconstruct import deconstructible
#from PIL import Image
#import PIL.ExifTags
from .functions import *
import subprocess, shutil
from django.core.files import File


@deconstructible
class PathAndRename_Video(object):
    """
    save new image/video in correct path
    """
    def __init__(self, sub_path):
        self.path = sub_path
    
    def __call__(self, instance, filename):
        Loc = instance.locationid.locationname
        os.path.basename(filename)
        camera_id = instance.cameraid
        filename = str(instance.eventdate)+"_"+filename
        today = str(date.today())
        filepath = os.path.join(self.path,camera_id,Loc,today,filename)
        return filepath

@deconstructible
class PathAndRename_Image(object):
    """
    save new image/video in correct path
    """
    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        Loc = instance.eventid.locationid.locationname
        os.path.basename(filename)
        camera_id = instance.cameraid
        filename = str(instance.eventid.eventdate)+"_"+filename
        today = str(date.today())
        filepath = os.path.join(self.path,camera_id,Loc,today,filename)
        return filepath



@deconstructible
class PathAndRename_shared(object):
    """
    save new shared video in correct path
    """
    def __init__(self, sub_path):
        self.path = sub_path
    
    def __call__(self, instance, filename):
        Vid = Video.objects.get(videoid = instance.videoid.videoid)
        camera_id = Vid.cameraid
        Loc = Vid.locationid.locationname
        today = str(date.today())
        filename = str(Vid.eventdate)+"_"+os.path.basename(filename)
        filepath = os.path.join(self.path,camera_id,Loc,today,filename)
        return filepath



class Event(models.Model):
    """
    table for events
    """
    eventid = models.AutoField(db_column = "eventID", primary_key=True, editable = False)
    locationid = models.ForeignKey('Location', db_column = 'locationID', on_delete=models.CASCADE, null = True, editable = False)
    samplingprotocol = models.CharField(db_column='samplingProtocol', max_length=255, blank = True, null = True)  # Field name made lowercase.
    eventdate = models.DateTimeField(db_column='eventDate', blank=True, null=True, editable = False)  # Field name made lowercase.
    eventremarks = models.CharField(db_column='eventRemarks', max_length=255, blank=True, null=True)  # Field name made lowercase.


class Video(models.Model):
    filepath = models.FileField(storage=OverwriteStorage(), upload_to = PathAndRename_Video("videos/"))
    eventdate = models.DateTimeField(db_column='eventDate', blank=True, null=True)
    videoid = models.AutoField(db_column = "videoid", primary_key=True, editable = False)
    #deploymentid= models.ForeignKey('Deployments', db_column = 'deploymentID', on_delete=models.CASCADE)#, editable = False)
    locationid = models.ForeignKey('Location', db_column = 'locationID', on_delete=models.CASCADE, editable = False)
    cameraid = models.CharField(db_column='cameraid', max_length=255, blank=True, null=True )
    samplingprotocol = models.CharField(db_column='samplingProtocol', max_length=255, blank = True, null = True)
    comments = models.CharField(db_column='eventRemarks', max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.locationid = self.deploymentid.locationid
        super(Video, self).save()
 
class Sequence(models.Model):
    sequenceid = models.AutoField(db_column = "sequenceid", primary_key=True, editable = False)
    videoid = models.ForeignKey(Video, db_column = "videoid", on_delete=models.CASCADE)

class Image(models.Model):
    """
    table for Images
    """
    imageid = models.AutoField(db_column = "imageID", primary_key=True, editable = False)
    eventid =  models.ForeignKey(Event, db_column = 'eventID',on_delete=models.CASCADE)
    filepath = models.ImageField(storage=OverwriteStorage(), upload_to=PathAndRename_Image("images/"))
    sequenceid = models.ForeignKey(Sequence, db_column = 'sequenceid', blank=True, null=True, on_delete=models.CASCADE)
    cameraid = models.CharField(db_column='cameraid', max_length=255, blank=True, null=True )

class SharedVideo(models.Model):
    filepath = models.FileField(storage=OverwriteStorage(), upload_to = PathAndRename_shared("videos_to_share/"))
    videoid =  models.ForeignKey('Video', on_delete=models.CASCADE, db_column='videoid')


class Occurence(models.Model):
    """
    Ocuurences within an event
    """
    occurenceid = models.AutoField(db_column = "occurenceID", primary_key=True, editable = False)
    eventid = models.ForeignKey('Event', on_delete = models.CASCADE, db_column='eventID', null = True )  # Field name made lowercase.
    taxonid = models.ForeignKey('Taxon', db_column='taxonID', on_delete=models.CASCADE, null = True)  # Field name made lowercase.
    sexid = models.ForeignKey('Sex', on_delete=models.CASCADE, db_column='sexID',null = True)  # Field name made lowercase.
    lifestageid = models.ForeignKey('Lifestage', on_delete=models.CASCADE, db_column='lifeStageID', null = True)  # Field name made lowercase.
    behaviorid = models.ForeignKey('Behavior', on_delete=models.CASCADE, db_column='behaviorID', null = True)  # Field name made lowercase.
    individualcount = models.IntegerField(db_column='individualCount', default = 0)  # Field name made lowercase.
    

    class Meta:
        constraints = [
            models.UniqueConstraint(
            fields=['eventid', 'occurenceid'], name='unique_event_occurence_combination'
            )
        ]


