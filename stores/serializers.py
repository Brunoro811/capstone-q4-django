from accounts.models import AccountModel
from accounts.serializers import AccountSerializer
from rest_framework import serializers

from stores.models import StoreModel


class GenericStoreFields():
    class Meta:
        abstract=True
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
            "name": {"help_text": "Unique. Field is string"},
            "state": {"help_text": "Field is string"},
            "street": {"help_text": "Field is string"},
            "number": {"help_text": "Field is int"},
            "zip_code": {"help_text": "Field is string. Max 10 caracters"},
            "is_active": {"help_text": "Field is boolean"},
            "other_information": {"help_text": "Field is string. Max 150 caracters"},
        }

class StoreModelSerializer(serializers.ModelSerializer,GenericStoreFields):
    ...

class StoreModelByIdSerializer(serializers.ModelSerializer,GenericStoreFields):
    def to_representation(self, instance: StoreModel):
        sellers_to_store = AccountModel.objects.filter(is_seller=True)
        admins_to_store = AccountModel.objects.filter(is_admin=True)

        ret = super().to_representation(instance)
        ret["sellers"] = AccountSerializer(sellers_to_store, many=True).data
        ret["admins"] = AccountSerializer(admins_to_store, many=True).data

        return ret

class ActivateDeactivateStoreSerializer(serializers.ModelSerializer,GenericStoreFields):
    class Meta(GenericStoreFields.Meta):
        model = StoreModel
        fields = "__all__"

    def to_representation(self, instance):
        return {
            "detail": f"store {instance.name} activated"
            if instance.is_active
            else f"store {instance.name} deactivated"
        }

    