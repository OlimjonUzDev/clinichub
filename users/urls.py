from django.urls import path

from .views import (
    RegisterView, DashboardView, UserListView, MeView,
    RequestOTPView, VerifyOTPView,
)


urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('dashboard/', DashboardView.as_view()),
    path('users/', UserListView.as_view()),
    path('me/', MeView.as_view()),
    path('otp/request/', RequestOTPView.as_view()),
    path('otp/verify/', VerifyOTPView.as_view()),
]
