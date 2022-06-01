import pdb

from products.models import ProductModel
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListCreateAPIView, UpdateAPIView

from variations.exceptions import ProductDoesNotExists
from variations.models import VariationModel
from variations.permissions import (
    IsAdmin,
    ListCreateAuthenticatePermission,
    ListCreateAuthorizePermission,
)
from variations.serializers import (
    ListUpdateSerializer,
    UpdateProductVariationSerializer,
)


class ListCreateProductVariationView(ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [
        ListCreateAuthenticatePermission,
        ListCreateAuthorizePermission,
    ]
    queryset = VariationModel.objects.all()
    serializer_class = ListUpdateSerializer


class UpdateProductVariationView(UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]
    serializer_class = UpdateProductVariationSerializer
    queryset = VariationModel.objects.all()
    lookup_url_kwarg = "variation_id"

    def patch(self, request, *args, **kwargs):
        # pdb.set_trace()
        if "product_id" in request.data:
            product_exists = ProductModel.objects.filter(
                id=request.data["product_id"]
            ).exists()
            if not product_exists:
                raise ProductDoesNotExists
        return super().patch(request, *args, **kwargs)
