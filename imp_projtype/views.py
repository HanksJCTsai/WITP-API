from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .models import ProjType
from .serializers import ProjTypeySerializer

# Create your views here.


class ProjTypeViewSet(viewsets.ModelViewSet):
    serializer_class = ProjTypeySerializer
    queryset = ProjType.objects.filter()

    def get_permissions(self):
        # 決定哪些method需要哪些認證
        # GET不用
        if self.request.method in ["POST","PUT","PATCH","DELETE"]:
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.AllowAny()]

    @action(detail=False, methods=["post"])
    def query_projecttype(self, request, pk=None):
        req = request.data
        projecttype = req.get("project_type")
        queryset = ProjType.objects.raw(
            "SELECT id, project_type FROM imp_projtype WHERE UPPER(project_type) LIKE UPPER (%s) ORDER BY project_type ASC", ["%" + projecttype + "%"]
        )
        serializer = ProjTypeySerializer(queryset, many=True)
        return Response(serializer.data)
