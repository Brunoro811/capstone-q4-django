from django.urls import path

from variations.views import ListCreateProductVariationView, UpdateProductVariationView

urlpatterns = [
    path("products/variations/", ListCreateProductVariationView.as_view()),
    path(
        "products/variations/<variation_id>/", UpdateProductVariationView.as_view()
    ),
]
