# Delivery/serializers.py
from rest_framework import serializers
from .models import Delivery


class DeliverySerializer(serializers.ModelSerializer):

    class Meta:
        model = Delivery
        fields = ['receiver_name', 'comments', 'date']
        read_only_fields = ['timestamp']
