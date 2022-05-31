from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from products.models import ProductModel
from products.permissions import IsAdmin
from products.serializers import LisCreateProducts


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
