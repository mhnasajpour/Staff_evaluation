from django.urls import path
from . import views

app_name = 'playground'
urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('management/', views.Management.as_view(), name='management'),
    path('category/<str:category>', views.Question_answers.as_view(),
         name='question_answers'),
]
