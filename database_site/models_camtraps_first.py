from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from datetime import datetime, timedelta
from django.core.validators import MinValueValidator,MaxValueValidator
from django.core.exceptions import ValidationError
from .models_helpTables import Location, PreUpload
import os
from PIL import Image
import PIL.ExifTags
from exiffield.fields import ExifField
#from exif import Image
#from exiffield.getters import exifgetter

from exiffield.getters import exifgetter
from datetime import datetime


import pytz
utc=pytz.UTC





"""
class Media(models.Model):
    captureMethodChoices = (('motion detection','motion detection'),('time lapse','time lapse'),)
    mediaid = models.CharField(db_column='mediaID', max_length = 255, editable = False, unique = True)  # Field name made lowercase.
    deploymentid = models.ForeignKey('Deployments', on_delete=models.CASCADE, db_column='deploymentID', editable = False)  # Field name made lowercase.
    sequenceid = models.IntegerField(db_column='sequenceID', default = Media_Increment_sequence_id)  # Field name made lowercase.
    capturemethod = models.CharField(db_column='captureMethod', max_length=255, blank=True, null=True,choices=captureMethodChoices)  # Field name made lowercase.
    timestamp = models.DateTimeField(db_column = 'timestamp', editable = False)
    filepath = models.ImageField(upload_to=path_and_rename('images/'))
    #filename = models.CharField(db_column='fileName', max_length=255, blank=True, null=True,editable = False)  # Field name made lowercase.
    #filemediatype = models.CharField(db_column='fileMediatype', max_length = 255, editable = False)  # Field name made lowercase.
    #exifdata = ExifField(source='filepath' ,db_column='exifData', blank=True, null=True)  # Field name made lowercase.
    exifdata = models.CharField(max_length=255, db_column='exifData', blank=True, null=True)  # Field name made lowercase.
    favourite = models.CharField(max_length=255, blank=True, null=True)
    comments = models.CharField(max_length=255, blank=True, null=True, editable = False)
    #field_id = models.IntegerField(db_column='_id', primary_key=True, default = Media_Increment_field_id,editable = False)  # Field renamed because it started with '_'.
    field_id = models.AutoField(db_column = "_id", primary_key=True, editable = False)
    
    def save(self, *args, **kwargs):
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
            self.timestamp = date_object
        except:
            raise ValidationError("no date in exif data or datetime is in a wrong format")
        try:
            self.filemediatype = image.format
        except:
            raise ValidationError("format wrong ")
        try:
            serial_number = exif['BodySerialNumber']
        except:
            raise ValidationError("no serial number")
        camera_deployments = Deployments.objects.filter(cameraid = cameraid)
        try:
            camera_deployments = Deployments.objects.filter(cameraid = cameraid)
            
            for deployment in camera_deployments:
                start_time =  deployment.start.replace(tzinfo=utc)
                end_time =  deployment.end.replace(tzinfo=utc)
                curr_time = date_object.replace(tzinfo=utc)
                if start_time <= curr_time and end_time >= curr_time:
                    self.deploymentid = deployment
        except:
            raise ValidationError("deployment is wrong " + cameraid+ "  " + str(date_object))            
        self.mediaid =  str(self.timestamp)+str(self.filepath)
        self.filename = str(self.filepath).split("\\")[-1]
        super(Media, self).save()
    


    class Meta:
        managed = False
        db_table = 'Media'

# make sure uploading image is in chronological order
@receiver(pre_save, sender = Media)
def VerifyChronologicalUploading(sender, instance, **kwarg):
    try:
        LastUploadTime = sender.objects.filter(deploymentid = instance.deploymentid).order_by('timestamp').last()
    except:
        pass
    else:
        if LastUploadTime:
            LastUploadTime = LastUploadTime.timestamp.replace(tzinfo=utc)
            time = instance.timestamp.replace(tzinfo=utc)
            if LastUploadTime >= time:
                raise ValidationError("New upload was taken earlier than latest upload")

@receiver(signal=post_save, sender=PreUpload, dispatch_uid='add_Media_on_new_PreUpload')
def CreateMediaFromPreUpload(sender, instance, **kwargs):
    image = Image.open(instance.img)
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
    try:
        filemediatype = image.format
    except:
        raise ValidationError("format wrong ")
    try:
        serial_number = exif['BodySerialNumber']
    except:
        raise ValidationError("no serial number")
    camera_deployments = Deployments.objects.filter(cameraid = cameraid)
    try:
        camera_deployments = Deployments.objects.filter(cameraid = cameraid)
        for deployment in camera_deployments:
            start_time =  deployment.start.replace(tzinfo=utc)
            end_time =  deployment.end.replace(tzinfo=utc)
            curr_time = date_object.replace(tzinfo=utc)
            if start_time <= curr_time and end_time >= curr_time:
                deploymentid = deployment
    except:
        raise ValidationError("deployment is wrong " + cameraid+ "  " + str(date_object))
    #mediaid =  str(timestamp)+str(instance.img)
    filename = (str(instance.img).split("\\")[-1]).split("/")[-1]
    mediaid =  str(timestamp)+str(filename)
    print(filename)
    print(instance.img.path)
    #raise ValidationError(filename)
    Loc = deploymentid.locationid.locationid
    filename = str(timestamp)+"_"+filename
    camera_path = os.path.join(cameraid,Loc)
    long_path = os.path.join(camera_path,filename)
    filepath= os.path.join('images/', str(long_path))
    mediaid =  str(timestamp)+str(filename)
    new_media = Media(
            timestamp = timestamp,
            filepath = filepath,
            filemediatype = filemediatype,
            deploymentid = deploymentid,
            mediaid = mediaid,
            filename = filename
            )
    new_media.save()


def Deployment_Increment_field_id():
    last = Deployments.objects.all().order_by('deploymentid').last()
    if not last:
        return 1
    return int(last.deploymentid)+1

"""

class Deployments(models.Model):
    BaitChoices = (('none','none'),('scent','scent'),('food','food'),('visual','visual'),('acoustic','acoustic'),('other','other'),)
    FeatureTypeChoices = (('none','none'),('road paved','road paved'),('road dirt','road dirt'),('trail hiking','trail hiking'),('trail game','trail game'),('road underpass','road underpass'),('road bridge','road bridge'),('culvert','culvert'),('burrow','burrow'),('nest site','nest site'),('carcass','carcass'),('water source','water source'),('fruiting tree','fruiting tree'),('other','other'),)
    locationid = models.ForeignKey('Location', on_delete=models.CASCADE, db_column='locationID', blank=True, null=True)  # Field name made lowercase.
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

    def save(self, *args, **kwargs):
        self.longitutde=  (Location.objects.get(locationid=self.locationid.locationid)).decimallongtitude
        self.latitude = (Location.objects.get(locationid=self.locationid.locationid)).decimallatitude
        try:
            self.coordinateuncertainty = Location.objects.get(locationid=self.locationid.locationid).coordinateUncertaintyInMeters
        except:
            self.coordinateuncertainty = 0
        super(Deployments, self).save()
    
    class Meta:
        managed = False
        db_table = 'Deployments'


"""
class Observation(models.Model):
    ObservationTypeChoices = (('unclassified','unclassified'),('animal','animal'),('human','human'),('vehicle','vehicle'),('blank','blank'),('unknown','unknown'),)
    LigeStageChoices = (('unknown','unknown'),('adult','adult'),('subadult','subadult'),('juvenile','juvenile'),('offspring','offspring'))
    classificationMethodChoices = (('human','human'),('machine','machine'),)
    SexChoices = (('unknown','unknown'),('female','female'),('male','male'),) 
    BehaviorChoices = (( 'unknown', 'unknown' ),('walking','walking'),('running','running'),('playing','playing'),('eating','eating'),)
    observationid= models.IntegerField(db_column='observationID', default = IncrementObservationID,editable = False)  # Field name made lowercase.
    #sequenceid = models.ForeignKey(Media,on_delete=models.CASCADE , db_column='sequenceID',related_name='Media_sequenceid', editable = False, blank=True, null = True)  # Field name made lowercase
    deploymentid = models.ForeignKey(Deployments, on_delete=models.CASCADE, db_column='deploymentID', editable = False)  # Field name made lowercase.
    mediaid = models.ForeignKey(Media,on_delete=models.CASCADE , db_column='mediaID',blank = True, null = True,related_name='Media_mediaid')  # Field name made lowercase..
    #timestamp = models.DateTimeField(db_column = 'timestamp', editable=False)
    observationtype = models.CharField(db_column='observationType', max_length=255, choices=ObservationTypeChoices, default = 'unclassified')  # Field name made lowercase.
    camerasetup = models.CharField(db_column='cameraSetup', max_length=255, blank=True, null=True)  # Field name made lowercase.
    taxonid = models.ForeignKey('Taxon', on_delete=models.CASCADE, db_column='taxonID', default = 'unknown')  # Field name made lowercase.
    #scientificname = models.CharField(db_column='scientificName', max_length=255, blank=True, null=True,editable = False)  # Field name made lowercase.
    count = models.IntegerField(default = 0,validators=[MinValueValidator(0)])
    #countnew = models.IntegerField(db_column='countNew', blank=True, null=True,validators=[MinValueValidator(0)])  # Field name made lowercase.
    lifestage = models.CharField(max_length=255,db_column='lifeStage', choices = LigeStageChoices,default = 'unknown')  # Field name made lowercase.
    sex = models.CharField(max_length=255,db_column = 'sex',choices=SexChoices, default = 'unknown')
    behavior = models.CharField(max_length=255, db_column='behaviour', choices = BehaviorChoices, default = 'unknown')
    individualid = models.CharField(db_column='individualID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    classificationmethod = models.CharField(db_column='classificationMethod', max_length=255, blank=True, null=True, choices=classificationMethodChoices)  # Field name made lowercase.
    classifiedby = models.CharField(db_column='classifiedBy', max_length=255, blank=True, null=True)  # Field name made lowercase.
    classificationtimestamp = models.DateTimeField(db_column='classificationTimestamp', blank=True, null=True)  # Field name made lowercase.
    classificationconfidence = models.FloatField(db_column='classificationConfidence', blank=True, null=True,validators=[MinValueValidator(0), MaxValueValidator(1)])  # Field name made lowercase.
    comments = models.CharField(max_length=255, blank=True, null=True)
    field_id = models.IntegerField(db_column='_id', primary_key = True, default = IncrementObservationID,editable = False)  # Field renamed because it started with '_'.


    def save(self, *args, **kwargs):
        try:
            first = Media.objects.filter(sequenceid=self.mediaid.sequenceid).order_by('timestamp').first() #get first object from this sequence)
        except:
            raise ValidationError("no such mediaid as "+str(mediaid))
        self.timestamp = first.timestamp #set timestamp of observation to be the first timestamp in this sequence
        try: 
            self.scientificname = self.taxonid.scientificname #set scientific name from taxon table
        except:
            raise ValidationError("no such taxonid as "+str(self.taxonid))
        self.deploymentid = self.mediaid.deploymentid #set deployment from media table
        self.sequenceid = first #set sequenceid 
        super(Observation, self).save()
    
    class Meta:
        managed = False
        db_table = 'Observation'
        constraints = [
            models.UniqueConstraint(
                fields=['observationid', 'mediaid'], name='unique_media_sequence_observation_combination'
            )
        ]

"""