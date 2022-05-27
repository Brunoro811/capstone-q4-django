from django.urls import path

from accounts.views import AccountsListCreateUpdateAPIView, LoginPostView

urlpatterns = [
    path('accounts/', AccountsListCreateUpdateAPIView.as_view()),
    path('login/', LoginPostView.as_view()),
]
