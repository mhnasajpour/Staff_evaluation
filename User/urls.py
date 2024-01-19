from django.urls import path
from . import views

app_name = 'user'
urlpatterns = [
    path('', views.User_edit.as_view(), name='edit'),
    path('login/', views.user_login.as_view(), name='login'),
    path('logout/', views.user_logout.as_view(), name='logout'),
]
