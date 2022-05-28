from django.urls import path

import stores.views as views

urlpatterns = [
    path("stores/", views.ListCreateStores.as_view()),
    path("stores/<store_id>/", views.StoreByIdView.as_view()),

]
