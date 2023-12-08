from django.db import models


# Create your models here.
class Trajectory(models.Model):

    id = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=255, blank=True, null=True)
    file_path = models.CharField(max_length=255, blank=True, null=True)
    file_size = models.CharField(max_length=255, blank=True, null=True)
    nas_id = models.ForeignKey('NASBox.NASBox', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'trajectory'
