from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from .forms import UserRegisterForm, UserLoginForm
from .models import User


class UserRegisterView(SuccessMessageMixin, CreateView):
    """Регистрация нового пользователя"""
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    success_message = _('Registration successful! Please log in.')

    def form_valid(self, form):
        """Отправка приветственного email после регистрации"""
        response = super().form_valid(form)
        user = self.object

        # Отправка приветственного email
        try:
            send_mail(
                subject=_('Welcome to our online store!'),
                message=_(
                    f'Hello {user.email}!\n\n'
                    f'Thank you for registering in our online store. '
                    f'We are glad to see you among our customers!\n\n'
                    f'Best regards,\n'
                    f'Store Team'
                ),
                from_email=None,  # Используем DEFAULT_FROM_EMAIL из settings
                recipient_list=[user.email],
                fail_silently=True,
            )
        except Exception as e:
            # Если email не отправился - не прерываем регистрацию
            print(f"Failed to send welcome email: {e}")

        return response


class UserLoginView(SuccessMessageMixin, LoginView):
    """Авторизация пользователя"""
    form_class = UserLoginForm
    template_name = 'users/login.html'
    success_message = _('You have successfully logged in!')

    def get_success_url(self):
        return reverse_lazy('home')


class UserLogoutView(LogoutView):
    """Выход из системы"""
    next_page = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, _('You have successfully logged out!'))
        return super().dispatch(request, *args, **kwargs)


class UserProfileView(LoginRequiredMixin, UpdateView):
    """Редактирование профиля пользователя (дополнительное задание)"""
    model = User
    template_name = 'users/profile.html'
    fields = ['first_name', 'last_name', 'avatar', 'phone', 'country']
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, _('Profile updated successfully!'))
        return super().form_valid(form)