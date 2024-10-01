from django.urls import path
from events import views

urlpatterns = [
    path('', views.events, name='events'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('category/<str:category>/', views.category, name='eventcategory'),
    path('categories/', views.categories, name='categories'),
    path('search/', views.search, name='search'),
]