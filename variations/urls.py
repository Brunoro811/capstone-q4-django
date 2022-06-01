from django.urls import path

from variations.views import (ListCreateProductVariationView,
                              ListProductVariationByVariationIdView)

urlpatterns = [
    path("products/variations/", ListCreateProductVariationView.as_view()),
    path("products/variations/<variation_id>/", ListProductVariationByVariationIdView.as_view()),
]
