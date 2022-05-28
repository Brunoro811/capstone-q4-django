from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import RetrieveUpdateAPIView

from stores.exception import StoreNameAlreadyExists
from stores.models import StoreModel
from stores.permissions import IsAdmin
from stores.serializers import StoreModelByIdSerializer, StoreModelSerializer


class ListCreateStores(generics.ListCreateAPIView):
    permission_classes = [IsAdmin]
    authentication_classes = [TokenAuthentication]
    queryset = StoreModel.objects.all()
    serializer_class = StoreModelSerializer

    def post(self, request, *args, **kwargs):
        """
        This route is authenticated.
        
        Only an admin user can access.
        
        This route create a store.
        """
        store = (
            StoreModel.objects.filter(name=self.request.data.get("name")).exists()
        )
        if store:
            raise StoreNameAlreadyExists
        return super().post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        This route is authenticated.
        
        Only an admin user can access.
        
        This route lists all stores.
        """
        return super().get(request, *args, **kwargs)

class StoreByIdView(RetrieveUpdateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]

    queryset = StoreModel.objects.all()
    serializer_class = StoreModelByIdSerializer
    lookup_url_kwarg = "store_id"
