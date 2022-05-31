from django.urls import path

from variations.views import ListCreateProductVariationView

urlpatterns = [
    path("products/variations/", ListCreateProductVariationView.as_view()),
]
