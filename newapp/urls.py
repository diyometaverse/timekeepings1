from django.urls import path
from . import views

app_name = 'newapp'

urlpatterns = [
    path('', views.landingpage_view, name='landingpage'),
]