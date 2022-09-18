# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Ai(models.Model):
    aiid = models.IntegerField(db_column='aiID', primary_key=True)  # Field name made lowercase.
    aiversion = models.CharField(db_column='aiVersion', max_length=255, blank=True, null=True)  # Field name made lowercase.
    animal_threshold = models.FloatField(db_column='Animal_Threshold', blank=True, null=True)  # Field name made lowercase.
    classification_threshold = models.FloatField(db_column='Classification_Threshold', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AI'


class Annotators(models.Model):
    annotatorid = models.IntegerField(db_column='annotatorID', primary_key=True)  # Field name made lowercase.
    annotatorname = models.CharField(db_column='annotatorName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    assumedexpertiselevel = models.FloatField(db_column='assumedExpertiseLevel', blank=True, null=True)  # Field name made lowercase.
    yearofbirth = models.DateField(db_column='yearOfBirth', blank=True, null=True)  # Field name made lowercase.
    annotatorprogram = models.CharField(db_column='AnnotatorProgram', max_length=255, blank=True, null=True)  # Field name made lowercase.
    version = models.CharField(db_column='Version', max_length=255, blank=True, null=True)  # Field name made lowercase.
    parameters = models.CharField(db_column='Parameters', max_length=255, blank=True, null=True)  # Field name made lowercase.
    annotatortype = models.CharField(db_column='annotatorType', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Annotators'


class Behavior(models.Model):
    behaviorid = models.IntegerField(db_column='behaviorID', primary_key=True)  # Field name made lowercase.
    behaviortype = models.CharField(db_column='behaviorType', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Behavior'


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


class Event(models.Model):
    eventid = models.IntegerField(db_column='eventID', primary_key=True)  # Field name made lowercase.
    samplingprotocol = models.CharField(db_column='samplingProtocol', max_length=255)  # Field name made lowercase.
    eventdate = models.DateTimeField(db_column='eventDate', blank=True, null=True)  # Field name made lowercase.
    eventremarks = models.CharField(db_column='eventRemarks', max_length=255, blank=True, null=True)  # Field name made lowercase.
    locationid = models.ForeignKey('Location', models.DO_NOTHING, db_column='locationID', blank=True, null=True)  # Field name made lowercase.
    supraeventid = models.IntegerField(db_column='supraEventID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Event'


class Lifestage(models.Model):
    lifestageid = models.IntegerField(db_column='lifeStageID', primary_key=True)  # Field name made lowercase.
    lifestagetype = models.CharField(db_column='lifeStageType', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LifeStage'


class Location(models.Model):
    locationid = models.CharField(db_column='locationID', primary_key=True, max_length=255)  # Field name made lowercase.
    decimallatitude = models.FloatField(db_column='decimalLatitude', blank=True, null=True)  # Field name made lowercase.
    decimallongtitude = models.FloatField(db_column='decimalLongtitude', blank=True, null=True)  # Field name made lowercase.
    coordinateuncertaintyinmeters = models.IntegerField(db_column='coordinateUncertaintyInMeters', blank=True, null=True)  # Field name made lowercase.
    continen = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    county = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Location'


class Media(models.Model):
    mediaid = models.OneToOneField('Observation', models.DO_NOTHING, db_column='mediaID', primary_key=True)  # Field name made lowercase.
    deploymentid = models.ForeignKey(Deployments, models.DO_NOTHING, db_column='deploymentID')  # Field name made lowercase.
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


class Observation(models.Model):
    observationid = models.IntegerField(db_column='observationID')  # Field name made lowercase.
    deploymentid = models.ForeignKey(Deployments, models.DO_NOTHING, db_column='deploymentID', blank=True, null=True)  # Field name made lowercase.
    sequenceid = models.IntegerField(db_column='sequenceID')  # Field name made lowercase.
    mediaid = models.IntegerField(db_column='mediaID', primary_key=True)  # Field name made lowercase.
    timestamp = models.DateTimeField(blank=True, null=True)
    observationtype = models.CharField(db_column='observationType', max_length=255)  # Field name made lowercase.
    camerasetup = models.CharField(db_column='cameraSetup', max_length=255, blank=True, null=True)  # Field name made lowercase.
    taxonid = models.CharField(db_column='taxonID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    scientificname = models.CharField(db_column='scientificName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    count = models.IntegerField(blank=True, null=True)
    countnew = models.IntegerField(db_column='countNew', blank=True, null=True)  # Field name made lowercase.
    lifestage = models.CharField(db_column='lifeStage', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sex = models.CharField(max_length=255, blank=True, null=True)
    behaviour = models.CharField(max_length=255, blank=True, null=True)
    individualid = models.CharField(db_column='individualID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    classificationmethod = models.CharField(db_column='classificationMethod', max_length=255, blank=True, null=True)  # Field name made lowercase.
    classifiedby = models.CharField(db_column='classifiedBy', max_length=255, blank=True, null=True)  # Field name made lowercase.
    classificationtimestamp = models.DateTimeField(db_column='classificationTimestamp', blank=True, null=True)  # Field name made lowercase.
    classificationconfidence = models.FloatField(db_column='classificationConfidence', blank=True, null=True)  # Field name made lowercase.
    comments = models.CharField(max_length=255, blank=True, null=True)
    field_id = models.CharField(db_column='_id', max_length=255, blank=True, null=True)  # Field renamed because it started with '_'.

    class Meta:
        managed = False
        db_table = 'Observation'
        unique_together = (('mediaid', 'observationid'),)


class Occurence(models.Model):
    occurenceid = models.IntegerField(db_column='occurenceID')  # Field name made lowercase.
    eventid = models.OneToOneField(Event, models.DO_NOTHING, db_column='eventID', primary_key=True)  # Field name made lowercase.
    taxonid = models.IntegerField(db_column='taxonID')  # Field name made lowercase.
    individualcount = models.IntegerField(db_column='individualCount')  # Field name made lowercase.
    sexid = models.ForeignKey('Sex', models.DO_NOTHING, db_column='sexID')  # Field name made lowercase.
    lifestageid = models.ForeignKey(Lifestage, models.DO_NOTHING, db_column='lifeStageID')  # Field name made lowercase.
    behaviorid = models.ForeignKey(Behavior, models.DO_NOTHING, db_column='behaviorID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Occurence'
        unique_together = (('eventid', 'occurenceid'),)



class Grades(models.Model):
    annotatorid = models.ForeignKey(Annotators, models.DO_NOTHING, db_column='annotatorID')  # Field name made lowercase.
    taskid = models.ForeignKey('Tasks', models.DO_NOTHING, db_column='taskID')  # Field name made lowercase.
    eventid = models.OneToOneField('Occurence', models.DO_NOTHING, db_column='eventID', primary_key=True)  # Field name made lowercase.
    occurenceid = models.ForeignKey('Occurence', models.DO_NOTHING, db_column='occurenceID',related_name='+')  # Field name made lowercase.
    grade = models.FloatField()

    class Meta:
        managed = False
        db_table = 'Grades'
        unique_together = (('eventid', 'occurenceid', 'taskid', 'annotatorid'),)

class Sex(models.Model):
    sexid = models.IntegerField(db_column='sexID', primary_key=True)  # Field name made lowercase.
    sextype = models.CharField(db_column='sexType', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Sex'


class Tasks(models.Model):
    taskid = models.IntegerField(db_column='taskID', primary_key=True)  # Field name made lowercase.
    taskname = models.CharField(db_column='taskName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    taskdescription = models.CharField(db_column='taskDescription', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Tasks'


class Taxon(models.Model):
    taxonid = models.IntegerField(db_column='taxonID', primary_key=True)  # Field name made lowercase.
    scientificname = models.CharField(db_column='scientificName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    genericname = models.CharField(db_column='genericName', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Taxon'




class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'



#class UserSerializer(serializers.HyperlinkedModelSerializer):
#    class Meta:
#        model = User
#        fields = ['url', 'username', 'email', 'is_staff']

# ViewSets define the view behavior.
#class UserViewSet(viewsets.ModelViewSet):
#    queryset = User.objects.all()
#    serializer_class = UserSerializer



