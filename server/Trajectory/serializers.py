from rest_framework import serializers
from .models import Trajectory


class TrajectorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Trajectory
        fields = '__all__'
