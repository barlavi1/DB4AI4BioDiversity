from rest_framework import serializers


from database_site.models import Taxon
from database_site.models import Ai
from database_site.models import Lifestage
from database_site.models import Sex
from database_site.models import Tasks
from database_site.models import Annotators
from database_site.models import Deployments
from database_site.models import Event
from database_site.models import Media
from database_site.models import Observation
from database_site.models import Location
from database_site.models import Occurence
from database_site.models import Behavior
from database_site.models import Grades

class TaxonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Taxon
        #fields = ('taxonid', 'scientificname','genericname')
        fields = '__all__'

class AiSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ai
        #fields = ('aiid','aiversion','animal_threshold','classification_threshold')
        fields = '__all__'

class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
        #fields = ('locationid','decimallatitude','decimallongtitude','coordinateuncertaintyinmeters','continen','country','county')

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


class DeploymentsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Deployments
        fields = '__all__'
        #fields = ('deploymentid','locationid','longitutde','latitude','start','end','setupby','cameraid','cameramodel', 'camerainterval','cameraheight','cameratilt','cameraheading','detectiondistance','timestampissues','baituse','session','array','featuretype','habitat','tags','comments')



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


