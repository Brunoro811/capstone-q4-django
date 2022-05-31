from products import views
from django.urls import path

urlpatterns = [
    path("products/<product_id>/", views.GetUpdateProductView.as_view()),
]
