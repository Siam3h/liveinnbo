from django.urls import path
from . import views

urlpatterns = [
 # urls.py
    path('payment/<int:event_id>/', views.process_payment, name='process_payment'),
    path('verify_payment/', views.verify_payment, name='verify_payment'),
    path('thankyou/<int:transaction_id>/', views.thankyou, name='thankyou'),
]
