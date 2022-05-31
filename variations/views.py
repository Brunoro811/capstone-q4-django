from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListCreateAPIView

from variations.models import VariationModel
from variations.permissions import (
    ListCreateAuthenticatePermission,
    ListCreateAuthorizePermission,
)
from variations.serializers import ListUpdateSerializer


class ListCreateProductVariationView(ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [
        ListCreateAuthenticatePermission,
        ListCreateAuthorizePermission,
    ]
    queryset = VariationModel.objects.all()
    serializer_class = ListUpdateSerializer
