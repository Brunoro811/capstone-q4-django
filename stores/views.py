from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import RetrieveAPIView

from stores.models import StoreModel
from stores.permissions import IsAdmin
from stores.serializers import StoreModelSerializer


class StoreByIdView(RetrieveAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]

    queryset = StoreModel.objects.all()
    serializer_class = StoreModelSerializer
    lookup_url_kwarg = "store_id"
