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


class Event(models.Model):
    eventid = models.OneToOneField('Media', on_delete=models.CASCADE, db_column='eventID', primary_key=True,editable = False)  # Field name made lowercase.
    samplingprotocol = models.CharField(db_column='samplingProtocol', max_length=255)  # Field name made lowercase.
    eventdate = models.DateTimeField(db_column='eventDate', blank=True, null=True)  # Field name made lowercase.
    eventremarks = models.CharField(db_column='eventRemarks', max_length=255, blank=True, null=True)  # Field name made lowercase.
    locationid = models.ForeignKey('Location', models.DO_NOTHING, db_column='locationID', blank=True, null=True)  # Field name made lowercase.
    #supraeventid = models.IntegerField(db_column='supraEventID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Event'



class Occurence(models.Model):
    occurenceid = models.IntegerField(db_column='occurenceID')  # Field name made lowercase.
    eventid = models.ForeignKey(Event, models.DO_NOTHING, db_column='eventID')  # Field name made lowercase.
    taxonid = models.ForeignKey(Taxon, db_column='taxonID', on_delete=models.CASCADE)  # Field name made lowercase.
    individualcount = models.IntegerField(db_column='individualCount')  # Field name made lowercase.
    sexid = models.ForeignKey('Sex', on_delete=models.CASCADE, db_column='sexID')  # Field name made lowercase.
    lifestageid = models.ForeignKey(Lifestage, on_delete=models.CASCADE, db_column='lifeStageID')  # Field name made lowercase.
    behaviorid = models.ForeignKey(Behavior, on_delete=models.CASCADE, db_column='behaviorID')  # Field name made lowercase.
    #supraeventid = models.IntegerField(db_column='supraEventID', blank=True, null=True)  # Field name made lowercase.
    field_id = models.AutoField(db_column='_id', primary_key = True)  # Field renamed because it started with '_'.
    
    class Meta:
        managed = False
        db_table = 'Occurence'
        constraints = [
            models.UniqueConstraint(
                fields=['eventid', 'occurenceid'], name='unique_event_occurence_combination'
            )
        ]
        #unique_together = (('eventid', 'occurenceid'),)

class SupraEventTable(models.Model):
    supraeventid = models.IntegerField(db_column='supraeventid',  primary_key = True)
    start_datetime =  models.DateTimeField(db_column='start_datetime')
    end_datetime =  models.DateTimeField(db_column='end_datetime')
    taxonid = models.ForeignKey(Taxon, models.DO_NOTHING, db_column='taxonid')
    locationid= models.ForeignKey(Location, models.DO_NOTHING, db_column='locationid')

    class Meta:
        managed = False
        db_table = 'SupraEventTable'

class Grades(models.Model):
    annotatorid = models.ForeignKey(Annotators, models.DO_NOTHING, db_column='annotatorID')  # Field name made lowercase.
    taskid = models.ForeignKey('Tasks', models.DO_NOTHING, db_column='taskID')  # Field name made lowercase.
    eventid = models.OneToOneField('Occurence', models.DO_NOTHING, db_column='eventID', primary_key=True)  # Field name made lowercase.
    occurenceid = models.ForeignKey('Occurence', models.DO_NOTHING, db_column='occurenceID',related_name='+')  # Field name made lowercase.
    grade = models.FloatField()

    class Meta:
        managed = False
        db_table = 'Grades'
        unique_together = (('eventid', 'occurenceid', 'taskid', 'annotatorid'),)

@receiver(signal=post_save, sender=Media, dispatch_uid='add_event_on_new_media')
def function_to_run_task(sender, instance, **kwargs):
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
            locationid = instance.deploymentid.locationid
        )
    new_event.save()

