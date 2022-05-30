from rest_framework import serializers

from products.models import ProductModel


class GetUpdateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = "__all__"
