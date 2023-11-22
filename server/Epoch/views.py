# Create your views here.
from rest_framework import viewsets
from .models import Epoch
from .serializers import EpochSerializer


class EpochViewSet(viewsets.ModelViewSet):
    queryset = Epoch.objects.all()
    serializer_class = EpochSerializer
