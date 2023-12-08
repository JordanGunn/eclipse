# Create your views here.
from rest_framework import viewsets
from .models import LidarTile
from .serializers import LidarTileSerializer


class LidarTileViewSet(viewsets.ModelViewSet):
    queryset = LidarTile.objects.all()
    serializer_class = LidarTileSerializer
