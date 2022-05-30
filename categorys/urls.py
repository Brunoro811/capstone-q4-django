from django.urls import path

from categorys import views

urlpatterns = [
    path("categories/<category_id>/", views.GetUpdateCategoryView.as_view()),
    path("categories/", views.GetCategoriesView.as_view()),
]
