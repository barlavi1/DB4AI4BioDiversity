# Generated by Django 4.1.1 on 2022-09-15 16:43

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
                ('longitutde', models.FloatField(blank=True, null=True)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('coordinateuncertainty', models.IntegerField(blank=True, db_column='coordinateUncertainty', null=True)),
                ('start', models.DateTimeField(blank=True, null=True)),
                ('end', models.DateTimeField(blank=True, null=True)),
                ('setupby', models.CharField(blank=True, db_column='setupBy', max_length=255, null=True)),
                ('cameraid', models.CharField(blank=True, db_column='cameraID', max_length=255, null=True)),
                ('cameramodel', models.CharField(blank=True, db_column='cameraModel', max_length=255, null=True)),
                ('camerainterval', models.IntegerField(blank=True, db_column='cameraInterval', null=True)),
                ('cameraheight', models.IntegerField(blank=True, db_column='cameraHeight', null=True)),
                ('cameratilt', models.IntegerField(blank=True, db_column='cameraTilt', null=True)),
                ('cameraheading', models.IntegerField(blank=True, db_column='cameraHeading', null=True)),
                ('detectiondistance', models.IntegerField(blank=True, db_column='detectionDistance', null=True)),
                ('timestampissues', models.DateTimeField(blank=True, db_column='timestampIssues', null=True)),
                ('baituse', models.IntegerField(blank=True, db_column='baitUse', null=True)),
                ('session', models.CharField(blank=True, max_length=255, null=True)),
                ('array', models.CharField(blank=True, max_length=255, null=True)),
                ('featuretype', models.CharField(blank=True, db_column='featureType', max_length=255, null=True)),
                ('habitat', models.CharField(blank=True, max_length=255, null=True)),
                ('tags', models.CharField(blank=True, max_length=255, null=True)),
                ('comments', models.CharField(blank=True, max_length=255, null=True)),
                ('field_id', models.CharField(blank=True, db_column='_id', max_length=255, null=True)),
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
            name='Event',
            fields=[
                ('eventid', models.IntegerField(db_column='eventID', primary_key=True, serialize=False)),
                ('samplingprotocol', models.CharField(db_column='samplingProtocol', max_length=255)),
                ('eventdate', models.DateTimeField(blank=True, db_column='eventDate', null=True)),
                ('eventremarks', models.CharField(blank=True, db_column='eventRemarks', max_length=255, null=True)),
                ('supraeventid', models.IntegerField(blank=True, db_column='supraEventID', null=True)),
            ],
            options={
                'db_table': 'Event',
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
            name='Observation',
            fields=[
                ('observationid', models.IntegerField(db_column='observationID')),
                ('sequenceid', models.IntegerField(db_column='sequenceID')),
                ('mediaid', models.IntegerField(db_column='mediaID', primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(blank=True, null=True)),
                ('observationtype', models.CharField(db_column='observationType', max_length=255)),
                ('camerasetup', models.CharField(blank=True, db_column='cameraSetup', max_length=255, null=True)),
                ('taxonid', models.CharField(blank=True, db_column='taxonID', max_length=255, null=True)),
                ('scientificname', models.CharField(blank=True, db_column='scientificName', max_length=255, null=True)),
                ('count', models.IntegerField(blank=True, null=True)),
                ('countnew', models.IntegerField(blank=True, db_column='countNew', null=True)),
                ('lifestage', models.CharField(blank=True, db_column='lifeStage', max_length=255, null=True)),
                ('sex', models.CharField(blank=True, max_length=255, null=True)),
                ('behaviour', models.CharField(blank=True, max_length=255, null=True)),
                ('individualid', models.CharField(blank=True, db_column='individualID', max_length=255, null=True)),
                ('classificationmethod', models.CharField(blank=True, db_column='classificationMethod', max_length=255, null=True)),
                ('classifiedby', models.CharField(blank=True, db_column='classifiedBy', max_length=255, null=True)),
                ('classificationtimestamp', models.DateTimeField(blank=True, db_column='classificationTimestamp', null=True)),
                ('classificationconfidence', models.FloatField(blank=True, db_column='classificationConfidence', null=True)),
                ('comments', models.CharField(blank=True, max_length=255, null=True)),
                ('field_id', models.CharField(blank=True, db_column='_id', max_length=255, null=True)),
            ],
            options={
                'db_table': 'Observation',
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
            name='Media',
            fields=[
                ('mediaid', models.OneToOneField(db_column='mediaID', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='database_site.observation')),
                ('sequenceid', models.IntegerField(db_column='sequenceID')),
                ('capturemethod', models.CharField(blank=True, db_column='captureMethod', max_length=255, null=True)),
                ('timestamp', models.DateTimeField(blank=True, null=True)),
                ('filepath', models.CharField(blank=True, max_length=255, null=True)),
                ('filename', models.CharField(blank=True, db_column='fileName', max_length=255, null=True)),
                ('filemediatype', models.CharField(blank=True, db_column='fileMediatype', max_length=255, null=True)),
                ('exifdata', models.CharField(blank=True, db_column='exifData', max_length=255, null=True)),
                ('favourite', models.CharField(blank=True, max_length=255, null=True)),
                ('comments', models.CharField(blank=True, max_length=255, null=True)),
                ('field_id', models.CharField(blank=True, db_column='_id', max_length=255, null=True)),
            ],
            options={
                'db_table': 'Media',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Occurence',
            fields=[
                ('occurenceid', models.IntegerField(db_column='occurenceID')),
                ('eventid', models.OneToOneField(db_column='eventID', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='database_site.event')),
                ('taxonid', models.IntegerField(db_column='taxonID')),
                ('individualcount', models.IntegerField(db_column='individualCount')),
            ],
            options={
                'db_table': 'Occurence',
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
