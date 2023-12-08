from rest_framework import serializers
from .models import LidarTile

class LidarTileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LidarTile
        fields = '__all__'