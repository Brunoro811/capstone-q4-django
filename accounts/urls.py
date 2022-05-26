from django.urls import path

from accounts.views import login

urlpatterns = [
    path('login/', login,),
]
