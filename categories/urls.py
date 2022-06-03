from django.urls import path

from categories.views import GetUpdateCategoryView, ListCreateCategoryView

urlpatterns = [
    path("categories/", ListCreateCategoryView.as_view()),
    path("categories/<category_id>/", GetUpdateCategoryView.as_view()),
]
