from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListCreateAPIView

from variations.models import VariationModel
from variations.serializers import listUpdateSerializer


class ListCreateProductVariationView(ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = []
    queryset = VariationModel.objects.all()
    serializer_class = listUpdateSerializer
