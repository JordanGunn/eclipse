# Create your views here.
from rest_framework import viewsets
from .models import Trajectory
from .serializers import TrajectorySerializer


class TrajectoryViewSet(viewsets.ModelViewSet):
    queryset = Trajectory.objects.all()
    serializer_class = TrajectorySerializer
