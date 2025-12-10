from django.urls import path
from django.contrib.auth import views as auth_views
from .views import UserRegisterView, UserLoginView, UserProfileView

app_name = 'users'

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),  # 📍 ЭТА СТРОКА
    path('profile/', UserProfileView.as_view(), name='profile'),
]