from django.urls import path

from variations.views import (
    ListCreateProductVariationView,
    ListUpdateProductVariationByVariationIdView,
)

urlpatterns = [
    path("products/variations/", ListCreateProductVariationView.as_view()),
    path(
        "products/variations/<variation_id>/",
        ListUpdateProductVariationByVariationIdView.as_view(),
    ),
]
