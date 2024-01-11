from django.urls import path
from . import views

app_name = 'user'
urlpatterns = [
    path('login/', views.user_login.as_view(), name='login'),
    path('logout/', views.user_logout.as_view(), name='logout'),
]
