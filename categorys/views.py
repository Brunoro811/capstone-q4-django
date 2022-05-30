from rest_framework.generics import CreateAPIView

from categorys.models import CategoryModel
from categorys.serializers import CreateCategorySerializer


class CreateCategoryView(CreateAPIView):
    # authentication_classes = ...
    # permission_classes = ...
    serializer_class = CreateCategorySerializer
    queryset = CategoryModel.objects.all()
