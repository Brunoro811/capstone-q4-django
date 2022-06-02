from rest_framework.serializers import (
    IntegerField,
    ModelSerializer,
    Serializer,
    UUIDField,
)

from orders.models import OrdersModel


class VariationsInfoSerializer(Serializer):
    id = UUIDField()
    quantity = IntegerField()


class CreateOrderSerializer(ModelSerializer):
    class Meta:
        model = OrdersModel
        fields = ["variations"]

    variations = VariationsInfoSerializer(many=True)
