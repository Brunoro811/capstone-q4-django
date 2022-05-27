from accounts.models import AccountModel
from accounts.serializers import AccountSerializer
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

class StoreModelByIdSerializer(serializers.ModelSerializer):
   
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
            "updated_at"
        ]
        read_only_fields = ["id", "is_active", "created_at", "updated_at"]

    def to_representation(self, instance: StoreModel):
        sellers_to_store = AccountModel.objects.filter(is_seller=True)
        admins_to_store = AccountModel.objects.filter(is_admin=True)
        
        ret = super().to_representation(instance)
        ret["sellers"] = AccountSerializer(sellers_to_store, many=True).data
        ret["admins"] = AccountSerializer(admins_to_store, many=True).data

        return ret
        

