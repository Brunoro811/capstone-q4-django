from django.urls import path

from stores.views import ListCreateStores, StoreByIdView

urlpatterns = [
    path("stores/", ListCreateStores.as_view()),
    path('stores/<store_id>/', StoreByIdView.as_view()),
]
