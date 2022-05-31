import pdb

from categorys.models import CategoryModel
from rest_framework import serializers

from products.models import ProductModel


class LisCreateProducts(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = "__all__"

        extra_kwargs = {
            "category_id": {"write_only": True},
        }

    def to_internal_value(self, data):
        if "category" in data.keys():
            category = CategoryModel.objects.get_or_create(name=data.get("category"))[0]
            data["category_id"] = category.id
        return super().to_internal_value(data)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["category"] = instance.category_id.name
        return ret
