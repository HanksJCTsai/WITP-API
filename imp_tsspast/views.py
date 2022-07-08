from rest_framework import permissions, viewsets
from rest_framework.permissions import IsAdminUser

from .models import ImpTssPast
from .serializers import ImpTssPastSerializer

# Create your views here.


class ImpTssPastViewSet(viewsets.ModelViewSet):
    serializer_class = ImpTssPastSerializer
    queryset = ImpTssPast.objects.filter()

    def get_permissions(self):
        # 決定哪些method需要哪些認證
        # GET不用
        if self.request.method in ["POST","PUT","PATCH","DELETE"]:
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.AllowAny()]
