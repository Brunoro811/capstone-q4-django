from rest_framework.serializers import ModelSerializer

from variations.models import VariationModel


class ListUpdateSerializer(ModelSerializer):
    class Meta:
        model = VariationModel
        fields = "__all__"
