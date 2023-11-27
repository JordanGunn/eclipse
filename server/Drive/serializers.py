from rest_framework import serializers
from .models import Drive


class DriveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drive
        fields = ['id', 'nas_id', 'delivery_id', 'storage_total_gb', 'storage_used_gb', 'serial_number', 'file_count']

