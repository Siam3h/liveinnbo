from django.urls import path, include
from . import views

urlpatterns = [
    path('protected/', views.protected_view, name='protected'),  
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('social-auth/complete/', views.social_auth_complete, name='social_auth_complete'),
    path('user/admin/', views.user_admin_interface, name='user_admin'),
    path('profile/', views.profile_view, name='profile'),
    path('', include('django.contrib.auth.urls')),
]
