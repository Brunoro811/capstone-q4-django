from rest_framework import serializers

from accounts.models import AccountModel


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField()


class RetrieveUpdateOneSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountModel
        fields = "__all__"
