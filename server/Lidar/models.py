from django.db import models


# Create your models here.
class Lidar(models.Model):

    id = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=255, blank=True, null=True)
    file_path = models.CharField(max_length=255, blank=True, null=True)
    file_size = models.CharField(max_length=255, blank=True, null=True)
    x_min = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    x_max = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    y_min = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    y_max = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    lidar_type = models.CharField(max_length=1, blank=True, null=True)
    version = models.FloatField(blank=True, null=True)
    epsg_code = models.ForeignKey('SpatialReference.SpatialReference', models.DO_NOTHING, blank=True, null=True)
    nas_id = models.ForeignKey('NASBox.NASBox', models.DO_NOTHING, blank=True, null=True)
    trajectory_id = models.ForeignKey('Trajectory.Trajectory', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lidar'
