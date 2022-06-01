import pdb

from products.models import ProductModel
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView

from variations.exceptions import ProductDoesNotExists
from variations.models import VariationModel
from variations.permissions import (
    IsAdmin,
    ListCreateAuthenticatePermission,
    ListCreateAuthorizePermission,
)
from variations.serializers import (
    ListByIdSerializer,
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


class ListUpdateProductVariationByVariationIdView(RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [ListCreateAuthenticatePermission]
    queryset = VariationModel.objects.all()
    serializer_class = ListByIdSerializer
    lookup_url_kwarg = "variation_id"

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return UpdateProductVariationSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.request.method == "PATCH":
            return [IsAdmin()]
        return super().get_permissions()

    def patch(self, request, *args, **kwargs):
        if "product_id" in request.data:
            product_exists = ProductModel.objects.filter(
                id=request.data["product_id"]
            ).exists()
            if not product_exists:
                raise ProductDoesNotExists
        return super().patch(request, *args, **kwargs)
