from django.urls import path

from stores import views
from stores.views import StoreByIdView

urlpatterns = [
    path("stores/", views.ListCreateStores.as_view()),
    path("stores/activate/<store_id>/", views.ActivateStore.as_view()),
    path("stores/deactivate/<store_id>/", views.DeactivateStore.as_view()),
    path("stores/<store_id>/", StoreByIdView.as_view()),
]
