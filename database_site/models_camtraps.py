from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from datetime import datetime, timedelta
from django.core.validators import MinValueValidator,MaxValueValidator
from django.core.exceptions import ValidationError
from .models_helpTables import Location

def Media_Increment_field_id():
    last = Media.objects.all().order_by('field_id').last()
    if not last:
        return 1
    field_object = Media._meta.get_field('field_id')
    last = field_object.value_from_object(last)
    return int(last)+1


class Media(models.Model):
    captureMethodChoices = (('motion detection','motion detection'),('time lapse','time lapse'),)
    mediaid = models.IntegerField(db_column='mediaID')  # Field name made lowercase.
    deploymentid = models.ForeignKey('Deployments', on_delete=models.CASCADE, db_column='deploymentID')  # Field name made lowercase.
    sequenceid = models.IntegerField(db_column='sequenceID')  # Field name made lowercase.
    capturemethod = models.CharField(db_column='captureMethod', max_length=255, blank=True, null=True,choices=captureMethodChoices)  # Field name made lowercase.
    timestamp = models.DateTimeField(db_column = 'timestamp')
    filepath = models.CharField(max_length=255, db_column = 'filepath')
    filename = models.CharField(db_column='fileName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    filemediatype = models.CharField(db_column='fileMediatype', max_length=255)  # Field name made lowercase.
    exifdata = models.CharField(db_column='exifData', max_length=255, blank=True, null=True)  # Field name made lowercase.
    favourite = models.CharField(max_length=255, blank=True, null=True)
    comments = models.CharField(max_length=255, blank=True, null=True)
    field_id = models.IntegerField(db_column='_id', primary_key=True, default = Media_Increment_field_id,editable = False)  # Field renamed because it started with '_'.

    
    class Meta:
        managed = False
        db_table = 'Media'


@receiver(pre_save, sender = Media)
def VerifyChronologicalUploading(sender, instance, **kwarg):
    LastUploadTime = sender.objects.filter(deploymentid = instance.deploymentid).order_by('timestamp').last()
    if LastUploadTime:
        if LastUploadTime.timestamp > instance.timestamp:
            raise ValidationError("New upload was taken earlier than latest upload")



def Dep_Increment_field_id():
    last = Deployments.objects.all().order_by('field_id').last()
    if not last:
        return 1
    return last+1


class Deployments(models.Model):
    BaitChoices = (('none','none'),('scent','scent'),('food','food'),('visual','visual'),('acoustic','acoustic'),('other','other'),)
    FeatureTypeChoices = (('none','none'),('road paved','road paved'),('road dirt','road dirt'),('trail hiking','trail hiking'),('trail game','trail game'),('road underpass','road underpass'),('road bridge','road bridge'),('culvert','culvert'),('burrow','burrow'),('nest site','nest site'),('carcass','carcass'),('water source','water source'),('fruiting tree','fruiting tree'),('other','other'),)
    deploymentid = models.IntegerField(db_column='deploymentID', primary_key=True)  # Field name made lowercase.
    locationid = models.ForeignKey('Location', on_delete=models.CASCADE, db_column='locationID', blank=True, null=True)  # Field name made lowercase.
    locationname = models.CharField(db_column='locationName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    longitutde = models.FloatField(db_column='longitutde', editable = False)
    latitude = models.FloatField(db_column='latitude', editable = False)
    coordinateuncertainty = models.IntegerField(db_column='coordinateUncertainty', blank=True, null=True, editable = False)  # Field name made lowercase.
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


    def save(self, *args, **kwargs):
        self.longitutde=  (Location.objects.get(locationid=self.locationid.locationid)).decimallongtitude
        self.latitude = (Location.objects.get(locationid=self.locationid.locationid)).decimallatitude
        try:
            self.coordinateuncertainty = Location.objects.get(locationid=self.locationid.locationid).coordinateUncertaintyInMeters
        except:
            self.coordinateuncertainty = 1
        super(Deployments, self).save()
    
    class Meta:
        managed = False
        db_table = 'Deployments'


def IncrementObservationID():
    last = Observation.objects.all().order_by('field_id').last()
    if not last:
        return 1

    field_object = Observation._meta.get_field('field_id')
    last = field_object.value_from_object(last)
    return last+1 

class Observation(models.Model):
    ObservationTypeChoices = (('animal','animal'),('human','human'),('vehicle','vehicle'),('blank','blank'),('unknown','unknown'),('unclassified','unclassified'),)
    LigeStageChoices = (('adult','adult'),('subadult','subadult'),('juvenile','juvenile'),('offspring','offspring'),('unknown','unknown'),)
    classificationMethodChoices = (('human','human'),('machine','machine'),)
    SexChoices = (('female','female'),('male','male'),) 
    observationid= models.IntegerField(db_column='observationID')  # Field name made lowercase.
    sequenceid = models.ForeignKey(Media,on_delete=models.CASCADE , db_column='sequenceID',related_name='Media_sequenceid')  # Field name made lowercase
    deploymentid = models.ForeignKey(Deployments, on_delete=models.CASCADE, db_column='deploymentID', editable = False)  # Field name made lowercase.
    mediaid = models.ForeignKey(Media,on_delete=models.CASCADE , db_column='mediaID',blank = True, null = True,related_name='Media_mediaid')  # Field name made lowercase..
    timestamp = models.DateTimeField(db_column = 'timestamp', editable=False)
    observationtype = models.CharField(db_column='observationType', max_length=255, choices=ObservationTypeChoices)  # Field name made lowercase.
    camerasetup = models.CharField(db_column='cameraSetup', max_length=255, blank=True, null=True)  # Field name made lowercase.
    taxonid = models.ForeignKey('Taxon', on_delete=models.CASCADE, db_column='taxonID', blank=True, null=True)  # Field name made lowercase.
    scientificname = models.CharField(db_column='scientificName', max_length=255, blank=True, null=True,editable = False)  # Field name made lowercase.
    count = models.IntegerField(blank=True, null=True)
    countnew = models.IntegerField(db_column='countNew', blank=True, null=True,validators=[MinValueValidator(0)])  # Field name made lowercase.
    lifestage = models.CharField(max_length=255,db_column='lifeStage', blank=True, null=True, choices = LigeStageChoices)  # Field name made lowercase.
    sex = models.CharField(max_length=255,db_column = 'sex', blank=True, null=True,choices=SexChoices)
    behavior = models.ForeignKey('Behavior', db_column='behaviour', on_delete=models.CASCADE,  blank=True, null=True)
    individualid = models.CharField(db_column='individualID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    classificationmethod = models.CharField(db_column='classificationMethod', max_length=255, blank=True, null=True, choices=classificationMethodChoices)  # Field name made lowercase.
    classifiedby = models.CharField(db_column='classifiedBy', max_length=255, blank=True, null=True)  # Field name made lowercase.
    classificationtimestamp = models.DateTimeField(db_column='classificationTimestamp', blank=True, null=True)  # Field name made lowercase.
    classificationconfidence = models.FloatField(db_column='classificationConfidence', blank=True, null=True,validators=[MinValueValidator(0), MaxValueValidator(1)])  # Field name made lowercase.
    comments = models.CharField(max_length=255, blank=True, null=True)
    field_id = models.IntegerField(db_column='_id', primary_key = True, default = IncrementObservationID,editable = False)  # Field renamed because it started with '_'.


    def save(self, *args, **kwargs):
        first = Media.objects.filter(sequenceid=self.sequenceid.sequenceid).order_by('timestamp').first()
        self.timestamp = first.timestamp
        if self.taxonid:
            self.scientificname = self.taxonid.scientificname
        self.deploymentid = self.sequenceid.deploymentid
        super(Observation, self).save()

    class Meta:
        managed = False
        db_table = 'Observation'
        #unique_together = (('mediaid', 'observationid'),)
        constraints = [
            models.UniqueConstraint(
                fields=['observationid','sequenceid', 'mediaid'], name='unique_media_sequence_observation_combination'
            )
        ]


