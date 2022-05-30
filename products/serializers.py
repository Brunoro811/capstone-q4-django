from rest_framework import serializers

from products.models import ProductModel


class LisCreateProducts(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = "__all__"
