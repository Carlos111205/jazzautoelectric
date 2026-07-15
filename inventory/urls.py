from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('shop/', views.shop, name='shop'),
]
