from rest_framework import viewsets
from .serializers import VPmsDeleteJiraUserSerializer
from .models import VPmsDeleteJiraUser


# Create your views here.
class VPmsDeleteJiraUserViewSet(viewsets.ModelViewSet):
  serializer_class = VPmsDeleteJiraUserSerializer
  queryset = VPmsDeleteJiraUser.objects.filter()
  http_method_names = ['get', 'head']