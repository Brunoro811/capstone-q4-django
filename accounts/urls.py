from django.urls import path


from accounts.views import AccountsListCreateUpdateAPIView, LoginPostView, RetrieveUpdateOneView
urlpatterns = [
    path('login/', LoginPostView.as_view()),
    path('accounts/', AccountsListCreateUpdateAPIView.as_view()),
    path("accounts/<user_id>/", RetrieveUpdateOneView.as_view()),
]
