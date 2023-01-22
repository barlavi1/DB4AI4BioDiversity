
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from datetime import datetime, timedelta, date
from django.core.validators import MinValueValidator,MaxValueValidator
from django.contrib.gis.db import models as Geomodels
from django.contrib.gis.geos import Polygon, Point



class Sex(models.Model):
    """
    table for sex
    """
    sexid = models.AutoField(db_column='sexID', primary_key=True, editable = False)  # Field name made lowercase.
    sextype = models.CharField(db_column='sexType', max_length=255, blank=True, null=True)  # Field name made lowercase.

class Taxon(models.Model):
    """
    table for different taxons
    """
    taxonid = models.IntegerField(db_column='taxonID', primary_key=True, editable = True, blank = False, null = False)  # Field name made lowercase.
    scientificname = models.CharField(db_column='scientificName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    genericname = models.CharField(db_column='genericName', max_length=255, blank=True, null=True)  # Field name made lowercase.


class Behavior(models.Model):
    """
    behavior of occurence
    """
    behaviorid = models.AutoField(db_column='behaviorID', editable = False, primary_key=True)  # Field name made lowercase.
    behaviortype = models.CharField(db_column='behaviorType', max_length=255, blank=True, null=True)  # Field name made lowercase.


class Lifestage(models.Model):
    """
    life stage of occurence
    """
    lifestageid = models.AutoField(db_column='lifeStageID', editable = False, primary_key=True)  # Field name made lowercase.
    lifestagetype = models.CharField(db_column='lifeStageType', max_length=255, blank=True, null=True)  # Field name made lowercase.


class County(models.Model):
    countyname = models.CharField(db_column="countyName",max_length=255)
    countyPolygon =  Geomodels.PolygonField(db_column="county")

class Region(models.Model):
    regionname = models.CharField(db_column="regionName",max_length=255)
    regionPolygon = Geomodels.PolygonField(db_column="regionPolygob")
    county = models.ForeignKey(County, db_column = 'county',on_delete=models.CASCADE, default=None)

class Location(models.Model):
    """
    table for location of deployments
    """
    locationid = models.AutoField(db_column='locationID', primary_key = True)  # Field name made lowercase.
    decimallongtitude = models.DecimalField(db_column='decimalLongtitude',max_digits = 11, decimal_places = 8,validators=[MinValueValidator(-180.00000000), MaxValueValidator(180.00000000)],  blank=True, null=True)  # Field name made lowercase. 
    decimallatitude = models.DecimalField(db_column='decimalLatitude',max_digits = 10, decimal_places = 8, validators=[MinValueValidator(-90.00000000), MaxValueValidator(90.00000000)], blank=True, null=True)  # Field name made lowercase.
    coordinateuncertaintyinmeters = models.IntegerField(db_column='coordinateUncertaintyInMeters', blank=True, null=True)  # Field name made lowercase.
    county = models.ForeignKey(County,  on_delete = models.CASCADE, blank=True, null=True, db_column = 'county')     #max_length=255, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete = models.CASCADE, blank=True, null=True, db_column = 'region')
    locationname = models.CharField(max_length=255, blank=False, null=False, db_column='locationName')
    location_coords =  Geomodels.PointField(db_column = "location", editable = False)
    
    def save(self, *args, **kwargs):
        self.location_coords=Point(float(self.decimallongtitude) , float(self.decimallatitude))
        super(Location, self).save()




#class Ai(models.Model):
#    """
#    table for machine annotators
#    """
#    aiid = models.IntegerField(db_column='aiID', primary_key=True)  # Field name made lowercase.
#    aiversion = models.CharField(db_column='aiVersion', max_length=255, blank=True, null=True)  # Field name made lowercase.
#    animal_threshold = models.FloatField(db_column='Animal_Threshold', blank=True, null=True)  # Field name made lowercase.
#    classification_threshold = models.FloatField(db_column='Classification_Threshold', blank=True, null=True)  # Field name made lowercase.


#class Tasks(models.Model):
#    """
#    table for different annotation types (species, count, sex etc.)
#    """
#    taskid = models.IntegerField(db_column='taskID', primary_key=True, default = Tasks_Increment_field_id)  # Field name made lowercase.
#    taskname = models.CharField(db_column='taskName', max_length=255, blank=True, null=True)  # Field name made lowercase.
#    taskdescription = models.CharField(db_column='taskDescription', max_length=255, blank=True, null=True)  # Field name made lowercase.




#class Annotators(models.Model):
#    """
#    table for different annotators
#    """
#    annotatorid = models.IntegerField(db_column='annotatorID', primary_key=True)  # Field name made lowercase.
#    annotatorname = models.CharField(db_column='annotatorName', max_length=255, blank=True, null=True)  # Field name made lowercase.
#    assumedexpertiselevel = models.FloatField(db_column='assumedExpertiseLevel', blank=True, null=True)  # Field name made lowercase.
#    yearofbirth = models.DateField(db_column='yearOfBirth', blank=True, null=True)  # Field name made lowercase.
#    annotatorprogram = models.CharField(db_column='AnnotatorProgram', max_length=255, blank=True, null=True)  # Field name made lowercase.
#    version = models.CharField(db_column='Version', max_length=255, blank=True, null=True)  # Field name made lowercase.
#    parameters = models.CharField(db_column='Parameters', max_length=255, blank=True, null=True)  # Field name made lowercase.
#    annotatortype = models.CharField(db_column='annotatorType', max_length=255, blank=True, null=True)  # Field name made lowercase.
