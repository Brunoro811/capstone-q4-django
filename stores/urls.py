from django.urls import path

import stores.views as views

urlpatterns = [
    path("stores/", views.ListCreateStores.as_view()),
]
