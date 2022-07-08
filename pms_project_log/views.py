from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .serializers import PmsProjectLogSerializer
from pms_project.models import PmsProjectLog

# Create your views here.
class PmsProjectLogViewSet(viewsets.ModelViewSet):
  serializer_class = PmsProjectLogSerializer
  queryset = PmsProjectLog.objects.filter()

  @swagger_auto_schema(
    operation_summary='Get Project Log',
  )
  def list(self, request, *args, **kwargs):
    queryset = self.get_queryset()
    result = [
      PmsProjectLogSerializer(r).data
      for r in queryset
    ]
    return Response(result)