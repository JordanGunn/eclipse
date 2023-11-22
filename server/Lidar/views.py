# Create your views here.
from rest_framework import viewsets
from .models import Lidar
from .serializers import LidarSerializer


class LidarViewSet(viewsets.ModelViewSet):
    queryset = Lidar.objects.all()
    serializer_class = LidarSerializer
