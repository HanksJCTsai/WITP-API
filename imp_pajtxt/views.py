from rest_framework import permissions, viewsets
from rest_framework.permissions import IsAdminUser

from .models import PajTxt
from .serializers import PajTxtSerializer

# Create your views here.


class PajTxtViewSet(viewsets.ModelViewSet):
    serializer_class = PajTxtSerializer
    queryset = PajTxt.objects.filter()

    def get_permissions(self):
        # 決定哪些method需要哪些認證
        # GET不用
        if self.request.method in ["POST","PUT","PATCH","DELETE"]:
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.AllowAny()]
