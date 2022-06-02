from django.urls import path

from orders.views import ListCreateOrderView

urlpatterns = [
    path("orders/", ListCreateOrderView.as_view()),
]
