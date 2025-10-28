from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админ-панель для категорий"""

    list_display = ("id", "name")  # Показываем id и name в списке
    list_display_links = ("id", "name")  # Делаем ссылками для перехода
    search_fields = ("name", "description")  # Поиск по названию и описанию


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Админ-панель для продуктов"""

    list_display = ("id", "name", "price", "category")  # Показываем в списке
    list_display_links = ("id", "name")  # Ссылки для перехода
    list_filter = ("category",)  # Фильтрация по категории
    search_fields = ("name", "description")  # Поиск по названию и описанию
    list_per_page = 20  # Количество элементов на странице

    # Поля которые показываются при редактировании
    fieldsets = (
        (
            "Основная информация",
            {"fields": ("name", "description", "category", "price")},
        ),
        ("Дополнительно", {"fields": ("image",), "classes": ("collapse",)}),
        ("Даты", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )

    # Поля только для чтения
    readonly_fields = ("created_at", "updated_at")
