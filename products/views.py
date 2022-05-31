import pdb

from categorys.models import CategoryModel
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication

from products.models import ProductModel
from products.permissions import IsAdmin
from products.serializers import LisCreateProducts


class LisCreateProductsView(generics.ListCreateAPIView):
    permission_classes = [IsAdmin]
    authentication_classes = [TokenAuthentication]
    queryset = ProductModel.objects.all()
    serializer_class = LisCreateProducts

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
