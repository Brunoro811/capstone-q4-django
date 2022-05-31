from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from stores.models import StoreModel

from products.exceptions import StoreDoesNotExists
from products.models import ProductModel
from products.permissions import IsAdmin
from products.serializers import GetUpdateProductSerializer, LisCreateProducts


class LisCreateProductsView(generics.ListCreateAPIView):
    permission_classes = [IsAdmin]
    authentication_classes = [TokenAuthentication]
    queryset = ProductModel.objects.all()
    serializer_class = LisCreateProducts

    def get_permissions(self):
        if hasattr(self.request, "method"):
            if self.request.method == "GET":
                return [
                    IsAuthenticated(),
                ]
        return super().get_permissions()

    def post(self, request, *args, **kwargs):
        """
        This route is authenticated.
        Only an admin user can access.
        This route create a product.
        """

        return super().post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        This route is authenticated.
        Anyone logged can access.
        This route lists all products.
        """
        return super().get(request, *args, **kwargs)


class GetUpdateProductView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAdmin]
    authentication_classes = [TokenAuthentication]
    serializer_class = GetUpdateProductSerializer
    queryset = ProductModel.objects.all()
    lookup_url_kwarg = "product_id"

    def get_permissions(self):
        if hasattr(self.request, "method"):
            if self.request.method == "GET":
                return [IsAuthenticated()]
        return super().get_permissions()

    def patch(self, request, *args, **kwargs):
        product_exists = ProductModel.objects.filter(id=kwargs["product_id"]).exists()
        if product_exists:
            product = ProductModel.objects.get(id=kwargs["product_id"])
            store_exists = StoreModel.objects.filter(
                id=request.data.get("store_id")
            ).exists()

            if "store_id" in request.data.keys():
                if store_exists:
                    product.store_id = StoreModel.objects.get(
                        id=request.data.get("store_id")
                    )
                    product.save()
                else:
                    raise StoreDoesNotExists

        return super().patch(request, *args, **kwargs)
