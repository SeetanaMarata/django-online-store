from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Category(models.Model):
    """Модель категории товаров"""

    name = models.CharField(max_length=100, verbose_name="Наименование")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель продукта"""

    name = models.CharField(max_length=100, verbose_name="Наименование")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    image = models.ImageField(
        upload_to="products/", verbose_name="Изображение", blank=True, null=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name="Категория",
        blank=True,
        null=True,
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена за покупку"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата последнего изменения"
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name="Опубликован",
        help_text="Товар будет виден на сайте только если отмечен",
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Ссылаемся на кастомную модель пользователя
        on_delete=models.SET_NULL,
        verbose_name="Владелец",
        blank=True,
        null=True,
        related_name="products",
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["-created_at"]
        # ДОБАВЬТЕ разрешения:
        permissions = [
            ("can_unpublish_product", "Может отменять публикацию продукта"),
            ("can_change_description", "Может изменять описание продукта"),
            ("can_change_category", "Может изменять категорию продукта"),
        ]

    def __str__(self):
        return f"{self.name} - {self.price} руб."


class Contact(models.Model):
    """Модель контактных данных магазина"""

    name = models.CharField(max_length=100, verbose_name="Название магазина")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email")
    address = models.TextField(verbose_name="Адрес")
    working_hours = models.TextField(verbose_name="Режим работы")
    description = models.TextField(verbose_name="Описание магазина", blank=True)

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"

    def __str__(self):
        return self.name
