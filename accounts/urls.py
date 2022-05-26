from django.urls import path

from accounts.views import AccountsListCreateUpdateAPIView, login

urlpatterns = [
    path('accounts/', AccountsListCreateUpdateAPIView.as_view()),
    path('login/', login),
]
