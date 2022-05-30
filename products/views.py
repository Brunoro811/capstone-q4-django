from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

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
                return [
                    IsAuthenticated(),
                ]
        return super().get_permissions()
