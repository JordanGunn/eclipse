# Create your views here.
from rest_framework import viewsets
from .models import DerivedProduct
from .serializers import DerivedProductSerializer

class DerivedProductViewSet(viewsets.ModelViewSet):
    queryset = DerivedProduct.objects.all()
    serializer_class = DerivedProductSerializer