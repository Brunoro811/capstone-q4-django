from django.urls import path

import stores.views as views

urlpatterns = [
    path("stores/", views.ListCreateStores.as_view()),
    path("stores/activate/<store_id>/", views.ActivateStore.as_view()),
    path("stores/deactivate/<store_id>/", views.DeactivateStore.as_view()),
]
