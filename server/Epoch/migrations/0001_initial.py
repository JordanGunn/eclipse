# Generated by Django 4.2.5 on 2023-11-20 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Epoch',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('epoch_year', models.IntegerField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'epoch',
                'managed': False,
            },
        ),
    ]
