from django.urls import path

from categorys.views import ListCreateCategoryView, GetUpdateCategoryView

urlpatterns = [
    path("categories/", ListCreateCategoryView.as_view()),
    path("categories/<category_id>/", GetUpdateCategoryView.as_view()),
]
