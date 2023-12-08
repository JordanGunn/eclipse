from rest_framework import serializers
from .models import LidarStrip

class LidarStripSerializer(serializers.ModelSerializer):
    class Meta:
        model = LidarStrip
        fields = '__all__'