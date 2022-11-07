# Generated by Django 4.1.1 on 2022-11-03 13:48

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database_site', '0003_multipleimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Continent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('continentname', models.CharField(blank=True, db_column='continentName', max_length=255, null=True)),
                ('continent', django.contrib.gis.db.models.fields.PolygonField(db_column='continent', srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('countryname', models.CharField(blank=True, db_column='countryName', max_length=255, null=True)),
                ('country', django.contrib.gis.db.models.fields.PolygonField(db_column='country', srid=4326)),
                ('continent', models.ForeignKey(db_column='continent', default=None, on_delete=django.db.models.deletion.CASCADE, to='database_site.continent')),
            ],
        ),
        migrations.CreateModel(
            name='County',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('countyname', models.CharField(blank=True, db_column='countyName', max_length=255, null=True)),
                ('county', django.contrib.gis.db.models.fields.PolygonField(db_column='county', srid=4326)),
                ('country', models.ForeignKey(db_column='country', default=None, on_delete=django.db.models.deletion.CASCADE, to='database_site.country')),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('regionname', models.CharField(blank=True, db_column='regionName', max_length=255, null=True)),
                ('region', django.contrib.gis.db.models.fields.PolygonField(db_column='region', srid=4326)),
                ('county', models.ForeignKey(db_column='county', default=None, on_delete=django.db.models.deletion.CASCADE, to='database_site.county')),
            ],
        ),
    ]
