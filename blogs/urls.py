from django.urls import path
from blogs import views

urlpatterns = [
    path('', views.blog, name='blog'),
    path('blogpost/<str:slug>', views.blogpost, name='blogpost'),
    path('category/<str:category>', views.category, name='blogcategory'),
    path('categories/', views.categories, name='categories'),
    path('search/', views.search, name='search'),
]