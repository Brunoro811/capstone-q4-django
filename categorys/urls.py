from django.urls import path

from categorys.views import CreateCategoryView

urlpatterns = [
    path("categories/", CreateCategoryView.as_view()),
]
