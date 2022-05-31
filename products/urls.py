from django.urls import path

from products import views

urlpatterns = [
    path("products/", views.LisCreateProductsView.as_view()),
    path("products/<uuid:product_id>/", views.GetUpdateProductView.as_view()),
]
