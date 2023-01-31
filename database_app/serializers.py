from rest_framework import serializers
from database_site.models import *
#from database_site.models_queryObjects import *
import django_filters



class TaxonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Taxon
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = '__all__'
        #fields = ('locationid','locationname','decimallatitude','decimallongtitude','coordinateuncertaintyinmeters','location_coords')#'continent','country','county', 'point_field')

class BehaviorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Behavior
        fields = '__all__'

class LifestageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lifestage
        fields = '__all__'


class SexSerializer(serializers.ModelSerializer):#HyperlinkedModelSerializer):
    class Meta:
        model = Sex
        fields = '__all__'

class DeploymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deployment
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    #mediaid = serializers.CharField(source='eventid.mediaid')
    #medialink = serializers.ImageField(source='eventid.filepath')
    class Meta:
        model = Event
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class OccurrenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occurrence
        fields = '__all__'

class SequenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sequence
        fields = '__all__'

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'

class Region(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'

class CountySerializer(serializers.ModelSerializer):
    class Meta:
        model = County
        fields = '__all__'





