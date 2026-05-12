from django.urls import path
from . import views

app_name = 'ai_eval'

urlpatterns = [
    path('', views.evaluate_view, name='evaluate'),
    path('history/', views.history_view, name='history'),
    path('result/<int:pk>/', views.result_view, name='result'),
    path('delete/<int:pk>/', views.delete_evaluation, name='delete'),
]