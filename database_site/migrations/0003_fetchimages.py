# Generated by Django 4.1.1 on 2022-10-12 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database_site', '0002_delete_supraeventtable'),
    ]

    operations = [
        migrations.CreateModel(
            name='FetchImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(db_column='start')),
                ('end', models.DateTimeField(db_column='end')),
            ],
            options={
                'db_table': 'FetchImages',
                'managed': False,
            },
        ),
    ]
