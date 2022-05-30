from rest_framework.serializers import ModelSerializer

from categorys.models import CategoryModel


class GetUpdateCategorySerializer(ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = "__all__"


class CreateCategorySerializer(ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = "__all__"
        extra_kwargs = {
            "id": {"read_only": True},
            "name": {"help_text": "Category's name."},
        }
