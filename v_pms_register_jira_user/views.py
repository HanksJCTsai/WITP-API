from rest_framework import viewsets
from .serializers import VPmsRegisterJiraUserSerializer
from .models import VPmsRegisterJiraUser


# Create your views here.
class VPmsRegisterJiraUserViewSet(viewsets.ModelViewSet):
  serializer_class = VPmsRegisterJiraUserSerializer
  queryset = VPmsRegisterJiraUser.objects.filter()
  http_method_names = ['get', 'head']