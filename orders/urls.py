from django.urls import path

from orders.views import listCreateOrderView

urlpatterns = [
    path("orders/", listCreateOrderView.as_view()),
]
