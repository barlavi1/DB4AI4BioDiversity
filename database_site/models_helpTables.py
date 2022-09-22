
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from datetime import datetime, timedelta


class Sex(models.Model):
    sexid = models.IntegerField(db_column='sexID', primary_key=True)  # Field name made lowercase.
    sextype = models.CharField(db_column='sexType', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Sex'

class Ai(models.Model):
    aiid = models.IntegerField(db_column='aiID', primary_key=True)  # Field name made lowercase.
    aiversion = models.CharField(db_column='aiVersion', max_length=255, blank=True, null=True)  # Field name made lowercase.
    animal_threshold = models.FloatField(db_column='Animal_Threshold', blank=True, null=True)  # Field name made lowercase.
    classification_threshold = models.FloatField(db_column='Classification_Threshold', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AI'

class Taxon(models.Model):
    taxonid = models.IntegerField(db_column='taxonID', primary_key=True)  # Field name made lowercase.
    scientificname = models.CharField(db_column='scientificName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    genericname = models.CharField(db_column='genericName', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Taxon'

class Annotators(models.Model):
    annotatorid = models.IntegerField(db_column='annotatorID', primary_key=True)  # Field name made lowercase.
    annotatorname = models.CharField(db_column='annotatorName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    assumedexpertiselevel = models.FloatField(db_column='assumedExpertiseLevel', blank=True, null=True)  # Field name made lowercase.
    yearofbirth = models.DateField(db_column='yearOfBirth', blank=True, null=True)  # Field name made lowercase.
    annotatorprogram = models.CharField(db_column='AnnotatorProgram', max_length=255, blank=True, null=True)  # Field name made lowercase.
    version = models.CharField(db_column='Version', max_length=255, blank=True, null=True)  # Field name made lowercase.
    parameters = models.CharField(db_column='Parameters', max_length=255, blank=True, null=True)  # Field name made lowercase.
    annotatortype = models.CharField(db_column='annotatorType', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Annotators'


class Behavior(models.Model):
    behaviorid = models.IntegerField(db_column='behaviorID', primary_key=True)  # Field name made lowercase.
    behaviortype = models.CharField(db_column='behaviorType', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Behavior'

class Lifestage(models.Model):
    lifestageid = models.IntegerField(db_column='lifeStageID', primary_key=True)  # Field name made lowercase.
    lifestagetype = models.CharField(db_column='lifeStageType', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LifeStage'

class Location(models.Model):
    locationid = models.CharField(db_column='locationID', primary_key=True, max_length=255)  # Field name made lowercase.
    decimallatitude = models.FloatField(db_column='decimalLatitude', blank=True, null=True)  # Field name made lowercase.
    decimallongtitude = models.FloatField(db_column='decimalLongtitude', blank=True, null=True)  # Field name made lowercase.
    coordinateuncertaintyinmeters = models.IntegerField(db_column='coordinateUncertaintyInMeters', blank=True, null=True)  # Field name made lowercase.
    continen = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    county = models.CharField(max_length=255, blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'Location'

class Tasks(models.Model):
    taskid = models.IntegerField(db_column='taskID', primary_key=True)  # Field name made lowercase.
    taskname = models.CharField(db_column='taskName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    taskdescription = models.CharField(db_column='taskDescription', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Tasks'

