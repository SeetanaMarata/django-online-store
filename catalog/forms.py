from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
    # Кастомная валидация для цены
    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price <= 0:
            raise forms.ValidationError("Цена должна быть больше 0")
        if price > 1000000:
            raise forms.ValidationError("Цена не может превышать 1 000 000 руб.")
        return price

    # Кастомная валидация для названия
    def clean_name(self):
        name = self.cleaned_data.get("name")
        if len(name) < 2:
            raise forms.ValidationError("Название должно содержать минимум 2 символа")
        return name

    class Meta:
        model = Product
        fields = ["name", "description", "image", "category", "price"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите название товара (минимум 2 символа)",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Подробное описание товара",
                }
            ),
            "image": forms.FileInput(
                attrs={"class": "form-control", "accept": "image/*"}
            ),
            "category": forms.Select(attrs={"class": "form-control"}),
            "price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Цена в рублях (от 1 до 1 000 000)",
                    "min": "1",
                    "max": "1000000",
                    "step": "0.01",
                }
            ),
        }
        labels = {
            "name": "Название товара *",
            "description": "Описание *",
            "image": "Изображение",
            "category": "Категория *",
            "price": "Цена (руб.) *",
        }
        error_messages = {
            "name": {
                "required": "Пожалуйста, введите название товара",
            },
            "description": {
                "required": "Пожалуйста, добавьте описание товара",
            },
            "category": {
                "required": "Пожалуйста, выберите категорию",
            },
            "price": {
                "required": "Пожалуйста, укажите цену товара",
            },
        }
