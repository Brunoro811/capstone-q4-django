from products.models import ProductModel
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView

from variations.exceptions import ProductDoesNotExists
from variations.models import VariationModel
from variations.permissions import (ListCreateAuthenticatePermission,
                                    ListCreateAuthorizePermission)
from variations.serializers import (ListByIdSerializer, ListUpdateSerializer,
                                    UpdateProductVariationSerializer)


class ListCreateProductVariationView(ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [
        ListCreateAuthenticatePermission,
        ListCreateAuthorizePermission,
    ]
    queryset = VariationModel.objects.all()
    serializer_class = ListUpdateSerializer


class ListUpdateProductVariationByVariationIdView(RetrieveUpdateAPIView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [ListCreateAuthenticatePermission,ListCreateAuthorizePermission]
    queryset = VariationModel.objects.all()
    serializer_class = ListByIdSerializer
    lookup_url_kwarg = "variation_id"

    def patch(self, request, *args, **kwargs):

        self.serializer_class = UpdateProductVariationSerializer

        if "product_id" in request.data:
            product_exists = ProductModel.objects.filter(
                id=request.data["product_id"]
            ).exists()
            if not product_exists:
                raise ProductDoesNotExists
        return super().patch(request, *args, **kwargs)
