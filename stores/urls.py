from django.urls import path

from stores.views import StoreByIdView

urlpatterns = [
    path('stores/<store_id>/', StoreByIdView.as_view()),
]
