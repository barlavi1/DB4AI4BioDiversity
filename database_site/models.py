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
from datetime import datetime, timedelta
from .models_AUTH_PERMISSIONS import *
from .models_helpTables import *
from .models_camtraps import *
import pytz
utc=pytz.UTC



class Event(models.Model):
    eventid = models.OneToOneField('Media', on_delete=models.CASCADE, db_column='eventID', primary_key=True,editable = False )  # Field name made lowercase.
    samplingprotocol = models.CharField(db_column='samplingProtocol', max_length=255)  # Field name made lowercase.
    eventdate = models.DateTimeField(db_column='eventDate', blank=True, null=True)  # Field name made lowercase.
    eventremarks = models.CharField(db_column='eventRemarks', max_length=255, blank=True, null=True)  # Field name made lowercase.
    locationid = models.ForeignKey('Location', on_delete=models.CASCADE, db_column='locationID', blank=True, null=True)  # Field name made lowercase.
    supraeventid = models.IntegerField(db_column='supraEventID', blank=True, null=True, editable = False)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'Event'



def Occurence_Increment_field_id():
    last = Occurence.objects.all().order_by('field_id').last()
    if not last:
        return 1
    last = last.field_id
    return int(last)+1
                                

class Occurence(models.Model):
    occurenceid = models.IntegerField(db_column='occurenceID')  # Field name made lowercase.
    eventid = models.ForeignKey('Event', on_delete = models.CASCADE, db_column='eventID')  # Field name made lowercase.
    taxonid = models.ForeignKey('Taxon', db_column='taxonID', on_delete=models.CASCADE)  # Field name made lowercase.
    individualcount = models.IntegerField(db_column='individualCount')  # Field name made lowercase.
    sexid = models.ForeignKey('Sex', on_delete=models.CASCADE, db_column='sexID')  # Field name made lowercase.
    lifestageid = models.ForeignKey('Lifestage', on_delete=models.CASCADE, db_column='lifeStageID')  # Field name made lowercase.
    behaviorid = models.ForeignKey('Behavior', on_delete=models.CASCADE, db_column='behaviorID')  # Field name made lowercase.
    field_id = models.IntegerField(db_column='_id', primary_key = True, default = Occurence_Increment_field_id,editable = False)  # Field renamed because it started with '_'.



    class Meta:
        managed = False
        db_table = 'Occurence'
        constraints = [
            models.UniqueConstraint(
                fields=['eventid', 'occurenceid'], name='unique_event_occurence_combination'
            )
        ]




def Grades_Increment_field_id():
    last = Grades.objects.all().order_by('field_id').last()
    if not last:
        return 1
    last = last.field_id
    return int(last)+1

class Grades(models.Model):
    annotatorid = models.ForeignKey(Annotators, on_delete = models.CASCADE, db_column='annotatorid')  # Field name made lowercase.
    taskid = models.ForeignKey('Tasks', on_delete = models.CASCADE, db_column='taskid')  # Field name made lowercase.
    eventid = models.ForeignKey('Occurence', on_delete = models.CASCADE, db_column='eventID', related_name='Occurence_eventid')  # Field name made lowercase.
    occurenceid = models.ForeignKey('Occurence', on_delete = models.CASCADE, db_column='occurenceID', related_name = 'Occurence_occurenceid')  # Field name made lowercase.
    grade = models.FloatField()
    field_id = models.AutoField(db_column='_id', primary_key = True, default = Grades_Increment_field_id,editable = False)

    class Meta:
        managed = False
        db_table = 'Grades'
        unique_together = (('eventid', 'occurenceid', 'taskid', 'annotatorid'),)

@receiver(signal=post_save, sender=Media, dispatch_uid='add_event_on_new_media')
def CreateEventFromMedia(sender, instance, **kwargs):
    LastSupraEventID = Event.objects.all().order_by('supraeventid').last() # Get lase supraeventid
    try:
        LastTime = Media.objects.filter(deploymentid = instance.deploymentid).order_by('-timestamp')[1] # previous image of this camera and location (deployment)
        #print(LastTime.timestamp)
    except:  # this is the first image of this camera and location
        LastTime = instance.timestamp - timedelta(minutes=16) #last time = this time -16m, then supraeventid will be increased by 1 (a new supraeventid will be assigned to this image
    else:
        LastTime = LastTime.timestamp # last datetime of this camera and location (deployment)
    ThisTime = instance.timestamp.replace(tzinfo=utc) #this datetime of this camera and location (deployment)
    DeltaTime = (LastTime + timedelta(minutes=15)).replace(tzinfo=utc)
    print(ThisTime)
    print(DeltaTime)
    if not LastSupraEventID: # this is the first image (of all cameras and locations (deployments)
        SupraEventID=1
    #elif LastTime + timedelta(minutes=15);
    elif DeltaTime <= ThisTime: # this is a new supraeventid
        SupraEventID = int(LastSupraEventID.supraeventid)+1
    else: #this is the same supraeventid
        SupraEventID = int(LastSupraEventID.supraeventid)
    capturemethod = instance.capturemethod
    if instance.capturemethod == "motion detection":
        capturemethod = "camera trap"
    else:
        capturemethod = "camera trap"
    new_event = Event(
            eventid = instance,
            samplingprotocol = capturemethod,
            eventdate = instance.timestamp,
            eventremarks = instance.comments,
            locationid = instance.deploymentid.locationid,
            supraeventid = SupraEventID
        )
    new_event.save()

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



