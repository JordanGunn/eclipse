# Create your views here.
from rest_framework import viewsets
from .models import LidarStrip
from .serializers import LidarStripSerializer


class LidarStripViewSet(viewsets.ModelViewSet):
    queryset = LidarStrip.objects.all()
    serializer_class = LidarStripSerializer
