from django.db import models
from .models import Media, Taxon, Observation
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
import os
from django.conf import settings

def IncreaseID():
    last = FetchImages.objects.all().order_by('_id').last()
    if not last:
        return 1
    else:
        return int(last._id)+1

class FetchImages(models.Model):
    cameraid = models.CharField(db_column='cameraid', max_length=255)  # Field name made lowercase.
    start = models.DateTimeField(db_column='start')  # Field name made lowercase
    end = models.DateTimeField(db_column='end', blank = True, null = True)  # Field name made lowercase
    animal = models.CharField(max_length=255, db_column = 'animal')
    #image_path = models.OneToOneField(Media, on_delete = models.CASCADE, db_column = 'image_path', related_name = 'Media_filepath')
    image_path = models.CharField(max_length=255, db_column = 'image_path')
    _id = models.IntegerField(db_column = "_id", primary_key = True, default = IncreaseID)
    class Meta:
        managed = False
        db_table = 'FetchImages'


@receiver(signal=post_save, sender=Observation, dispatch_uid='add_FetchImaged_on_new_Observation')
def CreateFetchImagesFromObservation(sender, instance, **kwargs):
    #try:
        #lastid = FetchImages.objects.latest(field_name = '_id')._id
    #except:
        #lastid = 1
    #else:
        #lastid = int(lastid)+1
    new_FetchImage = FetchImages(
            cameraid = instance.deploymentid.cameraid,
            start = instance.mediaid.timestamp,
            #end = instance.deploymentid.end,
            animal = instance.taxonid.genericname,
            image_path = os.path.join(settings.MEDIA_ROOT, str(instance.mediaid.filepath))
            #image_path = instance.mediaid
            #_id = lastid
           # locationid = instance.deploymentid.locationid
        )
    new_FetchImage.save()
