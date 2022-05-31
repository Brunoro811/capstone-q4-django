from categorys.models import CategoryModel
from rest_framework import serializers

from products.models import ProductModel


class GetUpdateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = [
            "id",
            "name",
            "cost_value",
            "sale_value_retail",
            "sale_value_wholesale",
            "quantity_wholesale",
            "is_active",
            "store_id",
            "category_id",
        ]
        extra_kwargs = {"category_id": {"write_only": True}}

    def to_internal_value(self, data):
        if "category" in data.keys():
            category = CategoryModel.objects.get_or_create(name=data.get("category"))[0]
            self.instance.category_id = category
        return super().to_internal_value(data)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["category"] = instance.category_id.name
        return ret
