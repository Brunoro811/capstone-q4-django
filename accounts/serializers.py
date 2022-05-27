from rest_framework import serializers

from accounts.exceptions import SellerNotAuthorizedForThisActionException
from accounts.models import AccountModel


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
    
        model = AccountModel
        fields = (
            "id",
            "username",
            "is_admin",
            "is_seller",
            "email",
            "first_name",
            "last_name",
            "created_at",
            "store_id",
            "password"
        )

        extra_kwargs = {
            'id': {'read_only': True},
            'password' : {'write_only': True},
        }

    def checking_allowed_fields_for_seller(self,validated_data):
        
        restrict_fields_seller = ('password','first_name','last_name',)
        error = [ field for field in validated_data if not field in restrict_fields_seller ]
        
        if error:
            raise SellerNotAuthorizedForThisActionException(
                detail={
                    "detail":"seller not authorized for this action.",
                    "unauthorized_fields": error
                    })
    
    def create(self, validated_data):
        
        return AccountModel.objects.create_user(**validated_data)

    def update(self, instance, validated_data):

        if not instance.is_admin:
            self.checking_allowed_fields_for_seller(validated_data)

        return super().update(instance, validated_data)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
