import django
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication

from stores.exception import StoreNameAlreadyExists
from stores.models import StoreModel
from stores.permissions import IsAdmin
from stores.serializers import StoreModelSerializer


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
            StoreModel.objects.filter(name=self.request.get("name")).exists()
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
