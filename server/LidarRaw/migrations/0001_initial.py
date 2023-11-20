# Generated by Django 4.2.5 on 2023-11-20 19:51

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Lidar', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LidarRaw',
            fields=[
                ('id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='Lidar.lidar')),
                ('convex_hull', django.contrib.gis.db.models.fields.PolygonField(blank=True, null=True, srid=4326)),
                ('file_source_id', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'lidarraw',
                'managed': False,
            },
        ),
    ]
