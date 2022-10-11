from rest_framework import serializers
from database_site.models import *


class TaxonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Taxon
        fields = ('taxonid', 'scientificname','genericname')
        #fields = '__all__'

class AiSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ai
        #fields = ('aiid','aiversion','animal_threshold','classification_threshold')
        fields = '__all__'

class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Location
        #fields = '__all__'
        fields = ('locationid','decimallatitude','decimallongtitude','coordinateuncertaintyinmeters','continen','country','county')

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


class TasksSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tasks
        fields = '__all__'
        #fields = ('taskid','taskname','taskdescription')


class AnnotatorsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Annotators
        fields = '__all__'
        #fields = ('annotatorid','annotatorname','assumedexpertiselevel','yearofbirth','annotatorprogram','version','parameters','annotatortype')


class DeploymentsListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        Last = (Deployments.objects.latest('deploymentid')).deploymentid
        #test = (Location.objects.get(locationid = "Zavitan_Hydro_2")).locationid
        #raise ValidationError(len(test))
        for item in validated_data: 
            item['deploymentid']=int(Last)+1
            current_location = Location.objects.get(locationid=item['locationid'].locationid)
            #raise ValidationError(item['locationid'].locationid)
            item['longitutde'] = current_location.decimallongtitude
            item['latitude'] = current_location.decimallatitude
            item['coordinateuncertainty'] = current_location.coordinateuncertaintyinmeters
            Last = int(Last)+1

        deployment = [Deployments(**item) for item in validated_data]
        return Deployments.objects.bulk_create(deployment)


        



class DeploymentsSerializer(serializers.ModelSerializer):
    #def __init__(self, *args, **kwargs):
        #super(DeploymentsSerializer, self).__init__(many=True, *args, **kwargs)
    class Meta:
        model = Deployments
        fields = '__all__'
        list_serializer_class = DeploymentsListSerializer
        #fields = ('deploymentid','locationid','longitutde','latitude','start','end','setupby','cameraid','cameramodel', 'camerainterval','cameraheight','cameratilt','cameraheading','detectiondistance','timestampissues','baituse','session','array','featuretype','habitat','tags','comments')

        def to_representation(self, instance):
            self.fields['locationid'] = serializers.HyperlinkedRelatedField(view_name='locationid', read_only=True)
            return super(req_AddPostSerializer, self).to_representation(instance)

class GradesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Grades
        fields = '__all__'
        #fields = ('annotatorid','taskid','eventid','occurenceid','grade')


class EventSerializer(serializers.HyperlinkedModelSerializer):
    #eventid = serializers.HyperlinkedRelatedField(view_name='event-id', read_only=True)
    class Meta:
        model = Event
        fields = '__all__'
        #fields = ('eventremarks','eventdate','samplingprotocol')


class MediaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'
        #fields = ('mediaid','deploymentid','sequenceid', 'capturemethod','timestamp','filepath','filename','filemediatype', 'exifdata', 'favourite', 'comments')


class ObservationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Observation
        fields = '__all__'
        #fields = ('observationid','deploymentid','sequenceid','mediaid','timestamp','observationtype', 'camerasetup','taxonid','scientificname','count','countnew','lifestage','sex','behavior', 'individualid','classificationmethod','classifiedby','classificationtimestamp','classificationconfidence','comments')


class OccurenceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Occurence
        fields = '__all__'
        #fields = ('occurenceid','eventid', 'taxonid','individualcount','sexid','lifestageid','behaviorid')


