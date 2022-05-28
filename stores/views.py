from django.utils import timezone
from requests import Response
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView

from stores.exception import (
    StoreIsAlreadyActive,
    StoreIsAlreadyDeactivated,
    StoreNameAlreadyExists,
)
from stores.models import StoreModel
from stores.permissions import IsAdmin
from stores.serializers import ActivateDeactivateStoreSerializer, StoreModelSerializer


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
        store = StoreModel.objects.filter(name=self.request.data["name"]).exists()
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


class ActivateStore(generics.UpdateAPIView):
    permission_classes = [IsAdmin]
    authentication_classes = [TokenAuthentication]
    queryset = StoreModel.objects.all()
    lookup_url_kwarg = "store_id"
    serializer_class = ActivateDeactivateStoreSerializer

    def patch(self, request, *args, **kwargs):
        """
        Route for activate an deactivated store
        """
        store_exists = StoreModel.objects.filter(id=kwargs["store_id"]).exists()
        if store_exists:
            store = StoreModel.objects.filter(id=kwargs["store_id"]).first()
            if store.is_active:
                raise StoreIsAlreadyActive
            store.is_active = True
            store.updated_at = timezone.now()
            store.save()
        return super().patch(request, *args, **kwargs)


class DeactivateStore(generics.UpdateAPIView):
    permission_classes = [IsAdmin]
    authentication_classes = [TokenAuthentication]
    queryset = StoreModel.objects.all()
    lookup_url_kwarg = "store_id"
    serializer_class = ActivateDeactivateStoreSerializer

    def patch(self, request, *args, **kwargs):
        """
        Route for deactivate an activated store
        """
        store_exists = StoreModel.objects.filter(id=kwargs["store_id"]).exists()
        if store_exists:
            store = StoreModel.objects.filter(id=kwargs["store_id"]).first()
            if not store.is_active:
                raise StoreIsAlreadyDeactivated
            store.is_active = False
            store.updated_at = timezone.now()
            store.save()
        return super().patch(request, *args, **kwargs)
