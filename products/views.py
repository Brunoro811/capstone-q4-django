import pdb

from categorys.models import CategoryModel
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from stores.models import StoreModel

from products.models import ProductModel
from products.permissions import IsAdmin
from products.serializers import GetUpdateProductSerializer


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
            category_exists = CategoryModel.objects.filter(
                id=request.data.get("category_id")
            ).exists()
            if "store_id" in request.data.keys():
                if store_exists:
                    product.store_id = StoreModel.objects.get(
                        id=request.data.get("store_id")
                    )
                    product.save()
                else:
                    raise Exception
            if "category_id" in request.data.keys():
                if category_exists:
                    product.category_id = CategoryModel.objects.get(
                        id=request.data.get("category_id")
                    )
                    product.save()
                else:
                    raise Exception

        return super().patch(request, *args, **kwargs)
