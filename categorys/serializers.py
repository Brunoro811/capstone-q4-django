from rest_framework import serializers

from categorys.models import CategoryModel


class GetUpdateCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = "__all__"
class GetCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = "__all__"
