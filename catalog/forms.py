import os

from django import forms
from django.core.exceptions import ValidationError

from .models import Product


class ProductForm(forms.ModelForm):
    """Форма для создания и редактирования продуктов с валидацией"""

    # Константы для запрещенных слов
    FORBIDDEN_WORDS = [
        "казино",
        "криптовалюта",
        "крипта",
        "биржа",
        "дешево",
        "бесплатно",
        "обман",
        "полиция",
        "радар",
    ]

    class Meta:
        model = Product
        fields = ["name", "description", "category", "price", "image"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Стилизация всех полей через метод __init__
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

            # Кастомные placeholder'ы
            if field_name == "name":
                field.widget.attrs["placeholder"] = "Введите название продукта"
            elif field_name == "description":
                field.widget.attrs["placeholder"] = "Опишите продукт..."
            elif field_name == "price":
                field.widget.attrs["placeholder"] = "0.00"
                field.widget.attrs["step"] = "0.01"
                field.widget.attrs["min"] = "0"

            # Специальные стили для определенных полей
            if field_name == "image":
                field.widget.attrs["class"] = "form-control-file"
            elif isinstance(field, forms.BooleanField):
                field.widget.attrs["class"] = "form-check-input"

    def clean_name(self):
        """Валидация названия продукта"""
        name = self.cleaned_data.get("name", "").lower()

        for word in self.FORBIDDEN_WORDS:
            if word in name:
                raise ValidationError(
                    f'Название содержит запрещенное слово: "{word}". '
                    f"Используйте другие формулировки."
                )

        return self.cleaned_data["name"]

    def clean_description(self):
        """Валидация описания продукта"""
        description = self.cleaned_data.get("description", "").lower()

        for word in self.FORBIDDEN_WORDS:
            if word in description:
                raise ValidationError(
                    f'Описание содержит запрещенное слово: "{word}". '
                    f"Используйте другие формулировки."
                )

        return self.cleaned_data["description"]

    def clean_price(self):
        """Валидация цены - не может быть отрицательной"""
        price = self.cleaned_data.get("price")

        if price is not None and price < 0:
            raise ValidationError(
                "Цена не может быть отрицательной. "
                "Пожалуйста, введите корректное значение."
            )

        return price

    def clean_image(self):
        """Валидация загружаемого изображения"""
        image = self.cleaned_data.get("image")

        if image:
            # Проверка расширения файла
            valid_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"]
            ext = os.path.splitext(image.name)[1].lower()

            if ext not in valid_extensions:
                raise ValidationError(
                    f"Неподдерживаемый формат файла: {ext}. "
                    f'Поддерживаемые форматы: {", ".join(valid_extensions)}'
                )

            # Проверка размера файла (5 МБ = 5 * 1024 * 1024 байт)
            max_size = 5 * 1024 * 1024  # 5 MB
            if image.size > max_size:
                raise ValidationError(
                    f"Размер файла слишком большой ({image.size // 1024} KB). "
                    f"Максимальный размер: 5 MB."
                )

        return image
