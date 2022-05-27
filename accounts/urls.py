from django.urls import path

from accounts.views import AccountsListCreateUpdateAPIView, LoginPostView

urlpatterns = [
    path('login/', LoginPostView.as_view()),
    path('accounts/', AccountsListCreateUpdateAPIView.as_view()),
]
