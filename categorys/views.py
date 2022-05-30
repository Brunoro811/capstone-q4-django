from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import CreateAPIView

from categorys.exceptions import AlreadyRegisteredNameError
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

    def post(self, request, *args, **kwargs):
        category = self.get_queryset().filter(name__iexact=request.data.get("name"))

        if category.exists():
            raise AlreadyRegisteredNameError

        return super().post(request, *args, **kwargs)
