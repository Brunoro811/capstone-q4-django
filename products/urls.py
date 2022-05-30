from django.urls import path

from products import views

urlpatterns = [
    path("product/", views.LisCreateProducts.as_view()),
]
