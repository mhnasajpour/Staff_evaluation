from django.urls import path
from . import views

app_name = 'playground'
urlpatterns = [
    path('', views.home.as_view(), name='home'),
]
