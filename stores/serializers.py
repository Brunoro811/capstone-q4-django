from django.utils import timezone
from rest_framework import serializers

from stores.models import StoreModel


class StoreModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreModel
        fields = [
            "id",
            "name",
            "state",
            "street",
            "number",
            "zip_code",
            "is_active",
            "other_information",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "is_active", "created_at", "updated_at"]

    def create(self, validated_data):
        validated_data["updated_at"] = timezone.now()
        return super().create(validated_data)
