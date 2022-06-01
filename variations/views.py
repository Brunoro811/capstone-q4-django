from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView

from variations.models import VariationModel
from variations.permissions import (ListCreateAuthenticatePermission,
                                    ListCreateAuthorizePermission)
from variations.serializers import ListByIdSerializer, ListUpdateSerializer


class ListCreateProductVariationView(ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [
        ListCreateAuthenticatePermission,
        ListCreateAuthorizePermission,
    ]
    queryset = VariationModel.objects.all()
    serializer_class = ListUpdateSerializer

class ListProductVariationByVariationIdView(RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [ListCreateAuthenticatePermission]
    queryset = VariationModel.objects.all()
    serializer_class = ListByIdSerializer
    lookup_url_kwarg = "variation_id"
