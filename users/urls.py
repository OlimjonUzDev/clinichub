from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import RegisterView, DashboardView


urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('dashboard/', DashboardView.as_view()),
]
