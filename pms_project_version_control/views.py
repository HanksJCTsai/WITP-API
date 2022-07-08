from django.db import connection
from rest_framework import viewsets
from .models import PmsProjectVersionControl
from .serializers import PmsProjectVersionControlSerializer

# Create your views here.
class PmsProjectVersionControlViewSet(viewsets.ModelViewSet):
    serializer_class = PmsProjectVersionControlSerializer
    queryset = PmsProjectVersionControl.objects.filter()
