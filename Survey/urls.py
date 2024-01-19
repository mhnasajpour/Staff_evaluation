from django.urls import path
from . import views

app_name = 'survey'
urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('management/', views.Management.as_view(), name='management'),
    path('category/<str:category>', views.Question_answers.as_view(), name='question_answers'),
    path('survey/skip/<str:category>', views.Skip_surveys.as_view(), name='skip_surveys'),
    path('survey/renew/', views.Renew_surveys.as_view(), name='renew'),
]
