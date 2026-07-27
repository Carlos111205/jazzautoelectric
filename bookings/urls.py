from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.owner_login, name='owner_login'),
    path('register/', views.owner_register, name='owner_register'),
    path('logout/', views.owner_logout, name='owner_logout'),
]
