from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserRegisterForm(UserCreationForm):
    """Форма регистрации пользователя"""
    email = forms.EmailField(
        label=_('Email'),
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'example@mail.com',
            'autofocus': True,
        })
    )

    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Create a strong password'),
        })
    )

    password2 = forms.CharField(
        label=_('Password confirmation'),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Repeat your password'),
        })
    )

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Убираем поле username из формы
        if 'username' in self.fields:
            del self.fields['username']

        # Добавляем классы Bootstrap ко всем полям
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        """Проверка уникальности email"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError(_('A user with this email already exists.'))
        return email

    def save(self, commit=True):
        """Создание пользователя с email как username"""
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # Используем email как username
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    """Форма авторизации по email"""
    username = forms.EmailField(
        label=_('Email'),
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'example@mail.com',
            'autofocus': True,
        })
    )

    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter your password'),
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Меняем label с username на email
        self.fields['username'].label = _('Email')

        # Добавляем классы Bootstrap
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean(self):
        """Валидация формы авторизации"""
        cleaned_data = super().clean()
        return cleaned_data