import ipdb
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

        extra_kwargs = {
            "name":{"help_text": "Unique. Field is string"} ,
            "state":{"help_text": "Field is string"},
            "street":{"help_text": "Field is string"},
            "number":{"help_text": "Field is int"},
            "zip_code":{"help_text": "Field is string. Max 10 caracters"}, 
            "is_active":{"help_text": "Field is boolean"},
            "other_information":{"help_text": "Field is string. Max 150 caracters"},           
        }

    def create(self, validated_data):
        validated_data["updated_at"] = timezone.now()
        return super().create(validated_data)


class ActivateDeactivateStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreModel
        fields = "__all__"

    def to_representation(self, instance):
        return {
            "detail": f"store {instance.name} activated"
            if instance.is_active
            else f"store {instance.name} deactivated"
        }
