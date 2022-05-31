import pdb
from rest_framework import serializers
from categorys.models import CategoryModel

from products.models import ProductModel


class LisCreateProducts(serializers.ModelSerializer):
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
            # "category"
        ]

        extra_kwargs = {
            "category_id": {"write_only": True},
        }

    def create(self, validated_data):
        print("\n\n\n\n", validated_data, "\n\n\n\n")
        return super().create(validated_data)

    def to_representation(self, instance):
        # category = CategoryModel.objects.get_or_create(name=instance.category_id)[0]
        # ret = super().to_representation(instance)
        # ret["category"] = category.name
        # pdb.set_trace()
        # return ret
        return super().to_representation(instance)