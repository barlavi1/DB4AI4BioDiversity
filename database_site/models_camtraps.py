from django.db import models
from django.conf import settings
#from django.dispatch import receiver
#from django.db.models.signals import post_save, pre_save
#from datetime import datetime, timedelta
from django.core.validators import MinValueValidator,MaxValueValidator
from django.core.exceptions import ValidationError
from .models_helpTables import Location
#import os
#from PIL import Image
#import PIL.ExifTags
#from exiffield.fields import ExifField
#from exif import Image
#from exiffield.getters import exifgetter
#from django.contrib.gis.geos import Point, Polygon
#from exiffield.getters import exifgetter


#import pytz
#utc=pytz.UTC


#class MultipleImage(models.Model):
#    images = models.FileField()





class Deployment(models.Model):
    BaitChoices = (('none','none'),('scent','scent'),('food','food'),('visual','visual'),('acoustic','acoustic'),('other','other'),)
    FeatureTypeChoices = (('none','none'),('road paved','road paved'),('road dirt','road dirt'),('trail hiking','trail hiking'),('trail game','trail game'),('road underpass','road underpass'),('road bridge','road bridge'),('culvert','culvert'),('burrow','burrow'),('nest site','nest site'),('carcass','carcass'),('water source','water source'),('fruiting tree','fruiting tree'),('other','other'),)
    locationid = models.ForeignKey('Location', on_delete=models.CASCADE, db_column='locationID')  # Field name made lowercase.
    #locationname = models.CharField(db_column='locationName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    #longitutde = models.DecimalField(db_column='longitutde', max_digits = 11, decimal_places = 8, editable = False)
    #latitude = models.DecimalField(db_column='latitude', max_digits = 10, decimal_places = 8, editable = False)
    #coordinateuncertainty = models.IntegerField(db_column='coordinateUncertainty', blank=True, null=True, editable = False)  # Field name made lowercase.
    start = models.DateTimeField(db_column='start')
    end = models.DateTimeField(db_column='end')
    setupby = models.CharField(db_column='setupBy', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cameraid = models.CharField(db_column='cameraID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cameramodel = models.CharField(db_column='cameraModel', max_length=255, blank=True, null=True)  # Field name made lowercase.
    camerainterval = models.IntegerField(db_column='cameraInterval', blank=True, null=True, validators=[MinValueValidator(0)])  # Field name made lowercase.
    cameraheight = models.IntegerField(db_column='cameraHeight', blank=True, null=True, validators=[MinValueValidator(0)])  # Field name made lowercase.
    cameratilt = models.IntegerField(db_column='cameraTilt', blank=True, null=True,validators=[MinValueValidator(-90), MaxValueValidator(90)])  # Field name made lowercase.
    cameraheading = models.IntegerField(db_column='cameraHeading', blank=True, null=True,validators=[MinValueValidator(0), MaxValueValidator(360)])  # Field name made lowercase.
    detectiondistance = models.IntegerField(db_column='detectionDistance', blank=True, null=True,validators=[MinValueValidator(0)])  # Field name made lowercase.
    timestampissues = models.BooleanField(db_column='timestampIssues', blank=True, null=True)  # Field name made lowercase.
    baituse = models.IntegerField(db_column='baitUse', blank=True, null=True,choices = BaitChoices)  # Field name made lowercase.
    session = models.CharField(max_length=255, blank=True, null=True)
    array = models.CharField(max_length=255, blank=True, null=True)
    featuretype = models.CharField(db_column='featureType', max_length=255, blank=True, null=True,choices = FeatureTypeChoices, default = 'none')  # Field name made lowercase.
    habitat = models.CharField(max_length=255, blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, null=True)
    comments = models.CharField(max_length=255, blank=True, null=True)
    #field_id = AutoField(db_column = "_id", primary_key=True, default = 1)  # Field renamed because it started with '_'.
    deploymentid = models.AutoField(db_column = "deploymentid", primary_key=True, editable = False)



    #def save(self, *args, **kwargs):
        #self.longitutde=  (Location.objects.get(locationid=self.locationid.locationid)).decimallongtitude
        #self.latitude = (Location.objects.get(locationid=self.locationid.locationid)).decimallatitude
        #try:
            #self.coordinateuncertainty = Location.objects.get(locationid=self.locationid.locationid).coordinateUncertaintyInMeters
        #except:
            #self.coordinateuncertainty = 0
        #super(Deployments, self).save()
    
#    class Meta:
#        managed = False
#        db_table = 'Deployments'




