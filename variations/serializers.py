from rest_framework.serializers import ModelSerializer

from variations.models import VariationModel


class GenericFields():
    
    class Meta:
        abstract = True
        model = VariationModel
        fields = '__all__'

        extra_kwargs = {
            "size": {"help_text": "Field is string, max 50 caracter."},
            "quantity": {"help_text": "Field is integer."},
            "color": {"help_text": "Field is float,, max 150 caracter."},
            "is_active": {"read_only": True},
            "product_id": {"help_text": "Field is UUID, foregnkey of products."},
        }

class ListUpdateSerializer(ModelSerializer,GenericFields):
    class Meta(GenericFields.Meta):
        abstract=False


class ListByIdSerializer(ModelSerializer,GenericFields):
    class Meta(GenericFields.Meta):
        abstract=False


class UpdateProductVariationSerializer(ModelSerializer,GenericFields):
    class Meta(GenericFields.Meta):
        abstract=False
