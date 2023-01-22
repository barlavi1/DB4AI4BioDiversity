from rest_framework import serializers
from database_site.models import *
#from database_site.models_queryObjects import *
import django_filters



class TaxonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Taxon
        fields = ('taxonid', 'scientificname','genericname')
        #fields = '__all__'

class LocationSerializer(serializers.HyperlinkedModelSerializer):
    #point_field = serializers.SerializerMethodField('InitPoint')

    #def InitPoint(self, instance):
        #return(Point(float(instance.decimallongtitude), float(instance.decimallatitude)))

    class Meta:
        model = Location
        #fields = '__all__'
        fields = ('locationid','locationname','decimallatitude','decimallongtitude','coordinateuncertaintyinmeters','location_coords')#'continent','country','county', 'point_field')

class BehaviorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Behavior
        fields = '__all__'
        #fields = ('behaviorid','behaviortype')



class LifestageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lifestage
        fields = '__all__'
        #fields = ('lifestageid', 'lifestagetype')


class SexSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sex
        fields = '__all__'
        #fields = ('sexid','sextype')

class DeploymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deployments
        fields = '__all__'
        #list_serializer_class = DeploymentsListSerializer
        #fields = ('deploymentid','locationid','longitutde','latitude','start','end','setupby','cameraid','cameramodel', 'camerainterval','cameraheight','cameratilt','cameraheading','detectiondistance','timestampissues','baituse','session','array','featuretype','habitat','tags','comments')

        #def to_representation(self, instance):
            #self.fields['locationid'] = serializers.HyperlinkedRelatedField(view_name='locationid', read_only=True)
            #return super(req_AddPostSerializer, self).to_representation(instance)


class EventSerializer(serializers.ModelSerializer):
    #mediaid = serializers.CharField(source='eventid.mediaid')
    #medialink = serializers.ImageField(source='eventid.filepath')
    class Meta:
        model = Event
        fields = '__all__'
        #fields = ('medialink','mediaid','eventremarks','eventdate','samplingprotocol', 'locationid','supraeventid')

class OccurenceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Occurence
        fields = '__all__'
        #fields = ('occurenceid','eventid', 'taxonid','individualcount','sexid','lifestageid','behaviorid')

class VideoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'

class Region(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'

class CountySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = County
        fields = '__all__'

class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class SequenceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sequence
        fields = '__all__'





