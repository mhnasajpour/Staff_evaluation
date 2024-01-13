from django.urls import path
from . import views

app_name = 'survey'
urlpatterns = [
    path('renew/', views.Renew_surveys.as_view(), name='renew'),
]
