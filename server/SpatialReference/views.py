# Create your views here.
from rest_framework import viewsets
from .models import SpatialReference
from .serializers import SpatialReferenceSerializer


class SpatialReferenceViewSet(viewsets.ModelViewSet):
    queryset = SpatialReference.objects.all()
    serializer_class = SpatialReferenceSerializer
