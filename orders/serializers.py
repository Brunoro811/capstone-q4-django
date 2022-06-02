from dataclasses import fields
from typing import List

from products.models import ProductModel
from rest_framework.serializers import (
    IntegerField,
    ModelSerializer,
    Serializer,
    SerializerMethodField,
    UUIDField,
)
from variations.models import VariationModel

from orders.models import OrdersModel


class VariationsInfoSerializer(Serializer):
    id = UUIDField()
    quantity = IntegerField()


class CreateOrderSerializer(ModelSerializer):
    class Meta:
        model = OrdersModel
        fields = ["variations"]

    variations = VariationsInfoSerializer(many=True)


class OrderProductSerializer(ModelSerializer):
    class Meta:
        model = ProductModel
        fields = "__all__"


class OrderProductsSerializer(ModelSerializer):
    class Meta:
        model = ProductModel
        fields = "__all__"

    def to_representation(self, instance: ProductModel):
        ret = super().to_representation(instance)

        ret.pop("category_id")
        ret.pop("is_active")

        ret["category"] = instance.category_id.name

        return ret


class OrderVariationsSerializer(ModelSerializer):
    class Meta:
        model = VariationModel
        fields = "__all__"


class CreateOrderResponseSerializer(ModelSerializer):
    seller_id = SerializerMethodField()
    store_id = SerializerMethodField()
    # variations = OrderVariationsSerializer(many=True)

    class Meta:
        model = OrdersModel
        fields = [
            "id",
            "created_at",
            "total_value",
            "seller_id",
            "store_id",
            # "products",
            # "variations",
        ]

    def get_seller_id(self, obj: OrdersModel):
        return obj.seller.id

    def get_store_id(self, obj: OrdersModel):
        return obj.store.id

    def get_products(self, obj: OrdersModel):
        return obj.variations

    def to_representation(self, instance: OrdersModel):
        ret = super().to_representation(instance)

        vars: list[VariationModel] = instance.variations.all()

        prods: List[ProductModel] = [var.product_id for var in vars]

        ret["products"] = OrderProductsSerializer(prods, many=True).data

        return ret
