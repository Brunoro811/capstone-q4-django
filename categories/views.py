from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from categories.exceptions import AlreadyRegisteredNameError
from categories.models import CategoryModel
from categories.permissions import (CreateAuthenticatePermission,
                                    CreateAuthorizePermission, IsAdmin)
from categories.serializers import (GetUpdateCategorySerializer,
                                    ListCreateCategorySerializer)


class ListCreateCategoryView(ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [CreateAuthenticatePermission, CreateAuthorizePermission]
    serializer_class = ListCreateCategorySerializer
    queryset = CategoryModel.objects.all()

    def get_permissions(self):
        if hasattr(self.request, "method"):
            if self.request.method == "GET":
                return [
                    IsAuthenticated(),
                ]
        return super().get_permissions()
    
    def post(self, request, *args, **kwargs):
        category = self.get_queryset().filter(name__iexact=request.data.get("name"))

        if category.exists():
            raise AlreadyRegisteredNameError

        return super().post(request, *args, **kwargs)


class GetUpdateCategoryView(RetrieveUpdateAPIView):
    permission_classes = [IsAdmin]
    authentication_classes = [TokenAuthentication]
    serializer_class = GetUpdateCategorySerializer
    queryset = CategoryModel.objects.all()
    lookup_url_kwarg = "category_id"

    def get_permissions(self):
        if hasattr(self.request, "method"):
            if self.request.method == "GET":
                return [
                    IsAuthenticated(),
                ]
        return super().get_permissions()

    
