from django.urls import path

from accounts.views import RetrieveUpdateOneView, login

urlpatterns = [
    path("login/", login),
    path("accounts/<user_id>/", RetrieveUpdateOneView.as_view()),
]
