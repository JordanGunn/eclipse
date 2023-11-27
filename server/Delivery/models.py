from django.db import models

# Create your models here.
class Delivery(models.Model):

    id = models.AutoField(primary_key=True)
    receiver_name = models.CharField(max_length=255, blank=True, null=True)
    comments = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Delivery {self.id}: {self.timestamp}"

    class Meta:
        managed = False
        db_table = 'delivery'
