from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import CreateAPIView

from categorys.models import CategoryModel
from categorys.permissions import (
    CreateAuthenticatePermission,
    CreateAuthorizePermission,
)
from categorys.serializers import CreateCategorySerializer


class CreateCategoryView(CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [CreateAuthenticatePermission, CreateAuthorizePermission]
    serializer_class = CreateCategorySerializer
    queryset = CategoryModel.objects.all()
