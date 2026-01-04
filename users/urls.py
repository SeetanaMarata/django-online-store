from django.contrib.auth import views as auth_views
from django.urls import path

from .views import UserLoginView, UserProfileView, UserRegisterView

app_name = "users"

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    # Исправляем logout - только POST запросы
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("profile/", UserProfileView.as_view(), name="profile"),
]
