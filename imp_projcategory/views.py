from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .models import ProjCategory
from .serializers import ProjCategorySerializer

# Create your views here.


class ProjCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = ProjCategorySerializer
    queryset = ProjCategory.objects.filter()

    def get_permissions(self):
        # 決定哪些method需要哪些認證
        # GET不用
        if self.request.method in ["POST","PUT","PATCH","DELETE"]:
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.AllowAny()]

    @action(detail=False, methods=["post"])
    def query_projectcategory(self, request, pk=None):
        req = request.data
        projectcategory = req.get("project_category")
        queryset = ProjCategory.objects.raw(
            "SELECT id, project_category FROM imp_projcategory WHERE UPPER(project_category) LIKE UPPER (%s) ORDER BY project_category ASC", ["%" + projectcategory + "%"]
        )
        serializer = ProjCategorySerializer(queryset, many=True)
        return Response(serializer.data)
