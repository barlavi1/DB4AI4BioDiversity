# Generated by Django 4.1.1 on 2022-09-22 07:53

import database_site.models_camtraps
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ai',
            fields=[
                ('aiid', models.IntegerField(db_column='aiID', primary_key=True, serialize=False)),
                ('aiversion', models.CharField(blank=True, db_column='aiVersion', max_length=255, null=True)),
                ('animal_threshold', models.FloatField(blank=True, db_column='Animal_Threshold', null=True)),
                ('classification_threshold', models.FloatField(blank=True, db_column='Classification_Threshold', null=True)),
            ],
            options={
                'db_table': 'AI',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Annotators',
            fields=[
                ('annotatorid', models.IntegerField(db_column='annotatorID', primary_key=True, serialize=False)),
                ('annotatorname', models.CharField(blank=True, db_column='annotatorName', max_length=255, null=True)),
                ('assumedexpertiselevel', models.FloatField(blank=True, db_column='assumedExpertiseLevel', null=True)),
                ('yearofbirth', models.DateField(blank=True, db_column='yearOfBirth', null=True)),
                ('annotatorprogram', models.CharField(blank=True, db_column='AnnotatorProgram', max_length=255, null=True)),
                ('version', models.CharField(blank=True, db_column='Version', max_length=255, null=True)),
                ('parameters', models.CharField(blank=True, db_column='Parameters', max_length=255, null=True)),
                ('annotatortype', models.CharField(blank=True, db_column='annotatorType', max_length=255, null=True)),
            ],
            options={
                'db_table': 'Annotators',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
            ],
            options={
                'db_table': 'auth_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_group_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('codename', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'auth_permission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.IntegerField()),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.IntegerField()),
                ('is_active', models.IntegerField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserGroups',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_user_groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserUserPermissions',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_user_user_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Behavior',
            fields=[
                ('behaviorid', models.IntegerField(db_column='behaviorID', primary_key=True, serialize=False)),
                ('behaviortype', models.CharField(blank=True, db_column='behaviorType', max_length=255, null=True)),
            ],
            options={
                'db_table': 'Behavior',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Deployments',
            fields=[
                ('deploymentid', models.IntegerField(db_column='deploymentID', primary_key=True, serialize=False)),
                ('locationname', models.CharField(blank=True, db_column='locationName', max_length=255, null=True)),
                ('longitutde', models.FloatField(db_column='longitutde')),
                ('latitude', models.FloatField(db_column='latitude')),
                ('coordinateuncertainty', models.IntegerField(blank=True, db_column='coordinateUncertainty', null=True)),
                ('start', models.DateTimeField(db_column='start')),
                ('end', models.DateTimeField(db_column='end')),
                ('setupby', models.CharField(blank=True, db_column='setupBy', max_length=255, null=True)),
                ('cameraid', models.CharField(blank=True, db_column='cameraID', max_length=255, null=True)),
                ('cameramodel', models.CharField(blank=True, db_column='cameraModel', max_length=255, null=True)),
                ('camerainterval', models.IntegerField(blank=True, db_column='cameraInterval', null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('cameraheight', models.IntegerField(blank=True, db_column='cameraHeight', null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('cameratilt', models.IntegerField(blank=True, db_column='cameraTilt', null=True, validators=[django.core.validators.MinValueValidator(-90), django.core.validators.MaxValueValidator(90)])),
                ('cameraheading', models.IntegerField(blank=True, db_column='cameraHeading', null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(360)])),
                ('detectiondistance', models.IntegerField(blank=True, db_column='detectionDistance', null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('timestampissues', models.BooleanField(blank=True, db_column='timestampIssues', default=False, null=True)),
                ('baituse', models.IntegerField(blank=True, choices=[('none', 'none'), ('scent', 'scent'), ('food', 'food'), ('visual', 'visual'), ('acoustic', 'acoustic'), ('other', 'other')], db_column='baitUse', default='none', null=True)),
                ('session', models.CharField(blank=True, max_length=255, null=True)),
                ('array', models.CharField(blank=True, max_length=255, null=True)),
                ('featuretype', models.CharField(blank=True, choices=[('none', 'none'), ('road paved', 'road paved'), ('road dirt', 'road dirt'), ('trail hiking', 'trail hiking'), ('trail game', 'trail game'), ('road underpass', 'road underpass'), ('road bridge', 'road bridge'), ('culvert', 'culvert'), ('burrow', 'burrow'), ('nest site', 'nest site'), ('carcass', 'carcass'), ('water source', 'water source'), ('fruiting tree', 'fruiting tree'), ('other', 'other')], db_column='featureType', default='none', max_length=255, null=True)),
                ('habitat', models.CharField(blank=True, max_length=255, null=True)),
                ('tags', models.CharField(blank=True, max_length=255, null=True)),
                ('comments', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'Deployments',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoAdminLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_time', models.DateTimeField()),
                ('object_id', models.TextField(blank=True, null=True)),
                ('object_repr', models.CharField(max_length=200)),
                ('action_flag', models.PositiveSmallIntegerField()),
                ('change_message', models.TextField()),
            ],
            options={
                'db_table': 'django_admin_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoContentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_label', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'django_content_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_session',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Lifestage',
            fields=[
                ('lifestageid', models.IntegerField(db_column='lifeStageID', primary_key=True, serialize=False)),
                ('lifestagetype', models.CharField(blank=True, db_column='lifeStageType', max_length=255, null=True)),
            ],
            options={
                'db_table': 'LifeStage',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('locationid', models.CharField(db_column='locationID', max_length=255, primary_key=True, serialize=False)),
                ('decimallatitude', models.FloatField(blank=True, db_column='decimalLatitude', null=True)),
                ('decimallongtitude', models.FloatField(blank=True, db_column='decimalLongtitude', null=True)),
                ('coordinateuncertaintyinmeters', models.IntegerField(blank=True, db_column='coordinateUncertaintyInMeters', null=True)),
                ('continen', models.CharField(blank=True, max_length=255, null=True)),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
                ('county', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'Location',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('mediaid', models.IntegerField(db_column='mediaID')),
                ('sequenceid', models.IntegerField(db_column='sequenceID')),
                ('capturemethod', models.CharField(blank=True, choices=[('motion detection', 'motion detection'), ('time lapse', 'time lapse')], db_column='captureMethod', max_length=255, null=True)),
                ('timestamp', models.DateTimeField(db_column='timestamp')),
                ('filepath', models.CharField(db_column='filepath', max_length=255)),
                ('filename', models.CharField(blank=True, db_column='fileName', max_length=255, null=True)),
                ('filemediatype', models.CharField(db_column='fileMediatype', max_length=255)),
                ('exifdata', models.CharField(blank=True, db_column='exifData', max_length=255, null=True)),
                ('favourite', models.CharField(blank=True, max_length=255, null=True)),
                ('comments', models.CharField(blank=True, max_length=255, null=True)),
                ('field_id', models.IntegerField(db_column='_id', default=database_site.models_camtraps.Media_Increment_field_id, editable=False, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'Media',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Observation',
            fields=[
                ('observationid', models.IntegerField(db_column='observationID')),
                ('timestamp', models.DateTimeField(db_column='timestamp', editable=False)),
                ('observationtype', models.CharField(choices=[('animal', 'animal'), ('human', 'human'), ('vehicle', 'vehicle'), ('blank', 'blank'), ('unknown', 'unknown'), ('unclassified', 'unclassified')], db_column='observationType', max_length=255)),
                ('camerasetup', models.CharField(blank=True, db_column='cameraSetup', max_length=255, null=True)),
                ('scientificname', models.CharField(blank=True, db_column='scientificName', editable=False, max_length=255, null=True)),
                ('count', models.IntegerField(blank=True, null=True)),
                ('countnew', models.IntegerField(blank=True, db_column='countNew', null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('lifestage', models.CharField(blank=True, choices=[('adult', 'adult'), ('subadult', 'subadult'), ('juvenile', 'juvenile'), ('offspring', 'offspring'), ('unknown', 'unknown')], db_column='lifeStage', max_length=255, null=True)),
                ('sex', models.CharField(blank=True, choices=[('female', 'female'), ('male', 'male')], db_column='sex', max_length=255, null=True)),
                ('individualid', models.CharField(blank=True, db_column='individualID', max_length=255, null=True)),
                ('classificationmethod', models.CharField(blank=True, choices=[('human', 'human'), ('machine', 'machine')], db_column='classificationMethod', max_length=255, null=True)),
                ('classifiedby', models.CharField(blank=True, db_column='classifiedBy', max_length=255, null=True)),
                ('classificationtimestamp', models.DateTimeField(blank=True, db_column='classificationTimestamp', null=True)),
                ('classificationconfidence', models.FloatField(blank=True, db_column='classificationConfidence', null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)])),
                ('comments', models.CharField(blank=True, max_length=255, null=True)),
                ('field_id', models.IntegerField(db_column='_id', default=database_site.models_camtraps.IncrementObservationID, editable=False, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'Observation',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Occurence',
            fields=[
                ('occurenceid', models.IntegerField(db_column='occurenceID')),
                ('individualcount', models.IntegerField(db_column='individualCount')),
                ('field_id', models.AutoField(db_column='_id', primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'Occurence',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Sex',
            fields=[
                ('sexid', models.IntegerField(db_column='sexID', primary_key=True, serialize=False)),
                ('sextype', models.CharField(blank=True, db_column='sexType', max_length=255, null=True)),
            ],
            options={
                'db_table': 'Sex',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SupraEventTable',
            fields=[
                ('supraeventid', models.IntegerField(db_column='supraeventid', primary_key=True, serialize=False)),
                ('start_datetime', models.DateTimeField(db_column='start_datetime')),
                ('end_datetime', models.DateTimeField(db_column='end_datetime')),
            ],
            options={
                'db_table': 'SupraEventTable',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('taskid', models.IntegerField(db_column='taskID', primary_key=True, serialize=False)),
                ('taskname', models.CharField(blank=True, db_column='taskName', max_length=255, null=True)),
                ('taskdescription', models.CharField(blank=True, db_column='taskDescription', max_length=255, null=True)),
            ],
            options={
                'db_table': 'Tasks',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Taxon',
            fields=[
                ('taxonid', models.IntegerField(db_column='taxonID', primary_key=True, serialize=False)),
                ('scientificname', models.CharField(blank=True, db_column='scientificName', max_length=255, null=True)),
                ('genericname', models.CharField(blank=True, db_column='genericName', max_length=255, null=True)),
            ],
            options={
                'db_table': 'Taxon',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('eventid', models.OneToOneField(db_column='eventID', editable=False, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='database_site.media')),
                ('samplingprotocol', models.CharField(db_column='samplingProtocol', max_length=255)),
                ('eventdate', models.DateTimeField(blank=True, db_column='eventDate', null=True)),
                ('eventremarks', models.CharField(blank=True, db_column='eventRemarks', max_length=255, null=True)),
            ],
            options={
                'db_table': 'Event',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Grades',
            fields=[
                ('eventid', models.OneToOneField(db_column='eventID', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='database_site.occurence')),
                ('grade', models.FloatField()),
            ],
            options={
                'db_table': 'Grades',
                'managed': False,
            },
        ),
    ]
