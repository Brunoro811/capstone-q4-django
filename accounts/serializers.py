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
            "password",
        )

        extra_kwargs = {
            'id': {'read_only': True},
            'password' : {
                            'write_only': True,
                            'help_text': 'Unrestricted string field'
                        },
            'is_admin': {"help_text": "Fields is boolean."},
            'is_seller': {"help_text": "Fields is boolean."},
            'email': {"help_text": "Unique. Field must be a valid email."},
            'first_name': {"help_text": "Maximum field length 150 characters."},
            'last_name': {"help_text": "Maximum field length 255 characters."},
            'username': {"help_text": "Unique. 150 characters or fewer. Letters, digits and @/./+/-/_ only."},  
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



class AccountUpdateSerializer(serializers.ModelSerializer):

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
            'password' : {'write_only': True,},
            
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

    def update(self, instance, validated_data):

        if not instance.is_admin:
            self.checking_allowed_fields_for_seller(validated_data)

        return super().update(instance, validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True,help_text="Field is string.")
    password = serializers.CharField(required=True,help_text="Field is string.")


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
        extra_kwargs = {
            'id': {'read_only': True},
            'password' : {
                            'write_only': True,
                            'help_text': 'Unrestricted string field'
                        },
            'is_admin': {"help_text": "Fields is boolean."},
            'is_seller': {"help_text": "Fields is boolean."},
            'email': {"help_text": "Unique. Field must be a valid email."},
            'first_name': {"help_text": "Maximum field length 150 characters."},
            'last_name': {"help_text": "Maximum field length 255 characters."},
            'username': {"help_text": "Unique. 150 characters or fewer. Letters, digits and @/./+/-/_ only."},  
        }

    def update(self, instance, validated_data):
        to_update_pass = validated_data.pop("password", None)
        if to_update_pass:
            instance.set_password(to_update_pass)
            instance.save()

        return super().update(instance, validated_data)
