from categories.models import CategoryModel
from rest_framework import serializers

from products.models import ProductModel


class GenericFields():
    
    class Meta:
        abstract = True
        model = ProductModel
        fields = '__all__'

        extra_kwargs = {
            "category_id": {"write_only": True},
            "name": {"help_text": "Field is string, max 255 caracter."},
            "sale_value_retail": {"help_text": "Field is float."},
            "sale_value_wholesale": {"help_text": "Field is float."},
            "quantity_wholesale": {"help_text": "Field is integer."},
            "cost_value": {"help_text": "Field is float."},
            "store_id": {"help_text": "Field is UUID, foregnkey of stores."},
            "category_id": {"help_text": "Field is UUID, foregnkey of categories."},
            "is_active": {"read_only": True},
        }


class LisCreateProducts(serializers.ModelSerializer,GenericFields):
    class Meta(GenericFields.Meta):
        abstract= False


    def to_internal_value(self, data):
        if "category" in data.keys():
            category = CategoryModel.objects.get_or_create(name=data.get("category"))[0]
            data["category_id"] = category.id
        return super().to_internal_value(data)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["category"] = instance.category_id.name
        return ret


class GetUpdateProductSerializer(serializers.ModelSerializer,GenericFields):
    class Meta(GenericFields.Meta):
        abstract= False
        

    def to_internal_value(self, data):
        if "category" in data.keys():
            category = CategoryModel.objects.get_or_create(name=data.get("category"))[0]
            self.instance.category_id = category
        return super().to_internal_value(data)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["category"] = instance.category_id.name
        return ret
