from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from categorys.models import CategoryModel
from categorys.permissions import IsAdmin
from categorys.serializers import (GetCategoriesSerializer,
                                   GetUpdateCategorySerializer)


class GetUpdateCategoryView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAdmin]
    authentication_classes = [TokenAuthentication]
    serializer_class = GetUpdateCategorySerializer
    queryset = CategoryModel.objects.all()
    lookup_url_kwarg = "category_id"
    
    def get_permissions(self):
        if hasattr(self.request, "method"):
            if self.request.method == "GET":
                return [IsAuthenticated(), ]
        return super().get_permissions()
class GetCategoriesView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = GetCategoriesSerializer
    queryset = CategoryModel.objects.all()

    
