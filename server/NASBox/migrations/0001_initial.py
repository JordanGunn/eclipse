# Generated by Django 4.2.5 on 2023-11-08 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NASBox',
            fields=[
                ('nas_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('location', models.CharField(max_length=255)),
                ('ipv4_addr', models.CharField(max_length=15)),
            ],
            options={
                'db_table': 'nasbox',
                'managed': False,
            },
        ),
    ]
