from rest_framework import serializers

from accounts.models import AccountModel


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField()


class RetrieveUpdateOneSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountModel
        fields = [
            "id",
            "email",
            "username",
            "password",
            "is_admin",
            "is_seller",
            "first_name",
            "last_name",
            "created_at",
            "store_id",
        ]
        read_only_fields = ["id", "created_at"]
        extra_kwargs = {"password": {"write_only": True}}

    def update(self, instance, validated_data):
        to_update_pass = validated_data.pop("password", None)
        if to_update_pass:
            instance.set_password(to_update_pass)
            instance.save()

        return super().update(instance, validated_data)
