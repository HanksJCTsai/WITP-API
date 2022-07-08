from django.db import connection
from rest_framework import viewsets
from .models import PmsProjectUser
from .serializers import PmsProjectUserSerializer

# Create your views here.
class PmsProjectUserViewSet(viewsets.ModelViewSet):
    serializer_class = PmsProjectUserSerializer
    queryset = PmsProjectUser.objects.filter()