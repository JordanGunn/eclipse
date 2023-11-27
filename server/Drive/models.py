# Create your models here.
from django.db import models


class Drive(models.Model):

    id = models.AutoField(primary_key=True)
    serial_number = models.CharField(max_length=255)
    storage_total_gb = models.DecimalField(max_digits=8, decimal_places=2)
    storage_used_gb = models.DecimalField(max_digits=8, decimal_places=2)
    file_count = models.IntegerField(blank=True, null=True)
    nas = models.ForeignKey('NASBox.NASBox', on_delete=models.CASCADE, blank=True, null=True)
    delivery = models.ForeignKey('Delivery.Delivery', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'drive'
