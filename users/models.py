from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Кастомная модель пользователя с email как username"""

    # Делаем email обязательным и уникальным
    email = models.EmailField(
        _('email address'),
        unique=True,
        blank=False,
        null=False,
        help_text=_('Required. Unique email address for authentication.')
    )

    # Дополнительные поля
    avatar = models.ImageField(
        _('avatar'),
        upload_to='users/avatars/',
        blank=True,
        null=True,
        help_text=_('User profile picture')
    )

    phone = models.CharField(
        _('phone number'),
        max_length=20,
        blank=True,
        help_text=_('Contact phone number')
    )

    country = models.CharField(
        _('country'),
        max_length=100,
        blank=True,
        help_text=_('Country of residence')
    )

    # Переопределяем поле для авторизации (вместо username используем email)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # username все еще нужен для админки

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-date_joined']

    def __str__(self):
        return self.email

    def get_full_name(self):
        """Возвращает полное имя пользователя"""
        full_name = f'{self.first_name} {self.last_name}'.strip()
        return full_name if full_name else self.email

    def clean(self):
        """Валидация модели"""
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)