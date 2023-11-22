# Create your views here.
from rest_framework import viewsets
from .models import ProcessingStatus
from .serializers import ProcessingStatusSerializer


class ProcessingStatusViewSet(viewsets.ModelViewSet):
    queryset = ProcessingStatus.objects.all()
    serializer_class = ProcessingStatusSerializer
