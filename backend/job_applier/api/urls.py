from django.urls import path
from .views import generate_email, send_email

urlpatterns = [
    path('generate/', generate_email, name='generate_email'),
    path('send/', send_email, name='send_email'),
]
