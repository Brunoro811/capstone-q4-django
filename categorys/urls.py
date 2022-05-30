from django.urls import path

from categorys.views import CreateCategoryView, GetUpdateCategoryView

urlpatterns = [
    path("categories/", CreateCategoryView.as_view()),
    path("categories/<category_id>/", GetUpdateCategoryView.as_view()),
]
