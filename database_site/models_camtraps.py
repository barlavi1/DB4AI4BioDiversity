from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from datetime import datetime, timedelta


class Media(models.Model):
    #CAPTURE_CHOICES = [(motion_detection, 'motion detection'), (time_lapse, 'time lapse')]
    mediaid = models.IntegerField(db_column='mediaID', primary_key=True)  # Field name made lowercase.
    deploymentid = models.ForeignKey('Deployments', on_delete=models.CASCADE, db_column='deploymentID')  # Field name made lowercase.
    sequenceid = models.IntegerField(db_column='sequenceID')  # Field name made lowercase.
    capturemethod = models.CharField(db_column='captureMethod', max_length=255, blank=True, null=True)  # Field name made lowercase.
    timestamp = models.DateTimeField(blank=True, null=True)
    filepath = models.CharField(max_length=255, blank=True, null=True)
    filename = models.CharField(db_column='fileName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    filemediatype = models.CharField(db_column='fileMediatype', max_length=255, blank=True, null=True)  # Field name made lowercase.
    exifdata = models.CharField(db_column='exifData', max_length=255, blank=True, null=True)  # Field name made lowercase.
    favourite = models.CharField(max_length=255, blank=True, null=True)
    comments = models.CharField(max_length=255, blank=True, null=True)
    field_id = models.CharField(db_column='_id', max_length=255, blank=True, null=True)  # Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'Media'

class Deployments(models.Model):
    deploymentid = models.IntegerField(db_column='deploymentID', primary_key=True)  # Field name made lowercase.
    locationid = models.ForeignKey('Location', models.DO_NOTHING, db_column='locationID')  # Field name made lowercase.
    locationname = models.CharField(db_column='locationName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    longitutde = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    coordinateuncertainty = models.IntegerField(db_column='coordinateUncertainty', blank=True, null=True)  # Field name made lowercase.
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    setupby = models.CharField(db_column='setupBy', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cameraid = models.CharField(db_column='cameraID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cameramodel = models.CharField(db_column='cameraModel', max_length=255, blank=True, null=True)  # Field name made lowercase.
    camerainterval = models.IntegerField(db_column='cameraInterval', blank=True, null=True)  # Field name made lowercase.
    cameraheight = models.IntegerField(db_column='cameraHeight', blank=True, null=True)  # Field name made lowercase.
    cameratilt = models.IntegerField(db_column='cameraTilt', blank=True, null=True)  # Field name made lowercase.
    cameraheading = models.IntegerField(db_column='cameraHeading', blank=True, null=True)  # Field name made lowercase.
    detectiondistance = models.IntegerField(db_column='detectionDistance', blank=True, null=True)  # Field name made lowercase.
    timestampissues = models.DateTimeField(db_column='timestampIssues', blank=True, null=True)  # Field name made lowercase.
    baituse = models.IntegerField(db_column='baitUse', blank=True, null=True)  # Field name made lowercase.
    session = models.CharField(max_length=255, blank=True, null=True)
    array = models.CharField(max_length=255, blank=True, null=True)
    featuretype = models.CharField(db_column='featureType', max_length=255, blank=True, null=True)  # Field name made lowercase.
    habitat = models.CharField(max_length=255, blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, null=True)
    comments = models.CharField(max_length=255, blank=True, null=True)
    field_id = models.CharField(db_column='_id', max_length=255, blank=True, null=True)  # Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'Deployments'


def IncrementObservationID():
  last_Observation = Observation.objects.all().order_by('field_id').last()
  if not last_Observation:
    return 1
  return last_Observation+1 

class Observation(models.Model):
    observationid = models.IntegerField(db_column='observationID')  # Field name made lowercase.
    #deploymentid = models.ForeignKey(Deployments, on_delete = models.CASCADE, db_column='deploymentID', editable = False)  # Field name made lowercase.
    sequenceid = models.IntegerField(db_column='sequenceID', editable = False)  # Field name made lowercase
    deploymentid = models.ForeignKey(Deployments, models.DO_NOTHING, db_column='deploymentID', blank=True, null=True)  # Field name made lowercase.
    sequenceid = models.IntegerField(db_column='sequenceID')  # Field name made lowercase.
    #mediaid = models.IntegerField(db_column='mediaID')  # Field name made lowercase
    #mediaid = models.OneToOneField('Media', models.DO_NOTHING, db_column='mediaID', primary_key = True)  # Field name made lowercase..
    mediaid = models.ForeignKey(Media, models.DO_NOTHING, db_column='mediaID')  # Field name made lowercase..
    timestamp = models.DateTimeField(blank=True, null=True)
    observationtype = models.CharField(db_column='observationType', max_length=255)  # Field name made lowercase.
    camerasetup = models.CharField(db_column='cameraSetup', max_length=255, blank=True, null=True)  # Field name made lowercase.
    #taxonid = models.CharField(db_column='taxonID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    taxonid = models.ForeignKey('Taxon', on_delete=models.CASCADE, db_column='taxonID')  # Field name made lowercase.
    scientificname = models.CharField(db_column='scientificName', max_length=255, blank=True, null=True,editable = False)  # Field name made lowercase.
    count = models.IntegerField(blank=True, null=True)
    countnew = models.IntegerField(db_column='countNew', blank=True, null=True)  # Field name made lowercase.
    lifestage = models.ForeignKey('Lifestage', db_column='lifeStage', on_delete = models.CASCADE, blank=True, null=True)  # Field name made lowercase.
    sex = models.ForeignKey('Sex', db_column='sex', on_delete = models.CASCADE, blank=True, null=True)
    behavior = models.ForeignKey('Behavior', db_column='behaviour', on_delete=models.CASCADE,  blank=True, null=True)
    individualid = models.CharField(db_column='individualID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    classificationmethod = models.CharField(db_column='classificationMethod', max_length=255, blank=True, null=True)  # Field name made lowercase.
    classifiedby = models.CharField(db_column='classifiedBy', max_length=255, blank=True, null=True)  # Field name made lowercase.
    classificationtimestamp = models.DateTimeField(db_column='classificationTimestamp', blank=True, null=True)  # Field name made lowercase.
    classificationconfidence = models.FloatField(db_column='classificationConfidence', blank=True, null=True)  # Field name made lowercase.
    comments = models.CharField(max_length=255, blank=True, null=True)
    field_id = models.AutoField(db_column='_id', primary_key = True, default = IncrementObservationID)  # Field renamed because it started with '_'.


    def save(self, *args, **kwargs):
        self.scientificname = self.taxonid.scientificname
        self.deploymentid = self.mediaid.deploymentid
        self.sequenceid = self.mediaid.sequenceid
        super(Observation, self).save()

    class Meta:
        managed = False
        db_table = 'Observation'
        #unique_together = (('mediaid', 'observationid'),)
        constraints = [
            models.UniqueConstraint(
                fields=['mediaid', 'observationid'], name='unique_media_observation_combination'
            )
        ]


