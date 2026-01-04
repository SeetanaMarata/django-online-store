from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Product, Category, Contact
from .forms import ProductForm


# Главная страница с пагинацией (FBV)
def home(request):
    """Главная страница с товарами и пагинацией"""
    # Новая версия: для обычных пользователей - опубликованные,
    # для модераторов и владельцев - все товары
    if request.user.is_authenticated and (
            request.user.has_perm("catalog.can_unpublish_product")
            or request.user.is_superuser
    ):
        # Модераторы видят ВСЕ товары
        products_list = Product.objects.all().order_by("-created_at")
    else:
        # Обычные пользователи видят только опубликованные
        products_list = Product.objects.filter(is_published=True).order_by(
            "-created_at"
        )

    # Пагинация - 6 товаров на страницу
    paginator = Paginator(products_list, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "catalog/home.html",
        {
            "page_obj": page_obj,
            "products": page_obj.object_list,
        },
    )


# Страница контактов (CBV)
class ContactsView(TemplateView):
    template_name = "catalog/contacts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем контактную информацию в контекст
        contact_info = Contact.objects.first()
        context["contact"] = contact_info
        return context


# Детальная страница товара (CBV)
class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


# Создание товара (CBV)
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        # Автоматически привязываем продукт к текущему пользователю
        form.instance.owner = self.request.user
        form.instance.is_published = False  # По умолчанию не опубликован
        messages.success(self.request, "Товар успешно создан! Ожидает модерации.")
        return super().form_valid(form)


# Редактирование товара (CBV)
class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("home")

    def test_func(self):
        """Проверяем, может ли пользователь редактировать продукт"""
        product = self.get_object()
        user = self.request.user

        # 1. Владелец может редактировать свой продукт
        # 2. Модератор может редактировать любой продукт
        # 3. Суперпользователь может всё
        return (
                product.owner == user
                or user.has_perm("catalog.can_unpublish_product")
                or user.is_superuser
        )

    def form_valid(self, form):
        messages.success(self.request, "Товар успешно обновлен!")
        return super().form_valid(form)


# Удаление товара (CBV)
class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("home")

    def test_func(self):
        """Проверяем, может ли пользователь удалить продукт"""
        product = self.get_object()
        user = self.request.user

        # 1. Владелец может удалить свой продукт
        # 2. Модератор может удалить любой продукт
        # 3. Суперпользователь может всё
        return (
                product.owner == user
                or user.has_perm("catalog.delete_product")
                or user.is_superuser
        )

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Товар успешно удален!")
        return super().delete(request, *args, **kwargs)


# Публикация товара (только для модераторов)
class ProductPublishView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Публикация продукта (только для модераторов)"""

    def test_func(self):
        """Проверяем, имеет ли пользователь право публиковать"""
        return self.request.user.has_perm("catalog.can_unpublish_product")

    def post(self, request, pk):
        """Обрабатываем POST-запрос на публикацию"""
        product = get_object_or_404(Product, pk=pk)
        product.is_published = True
        product.save()

        messages.success(request, f'Продукт "{product.name}" опубликован')
        return redirect("product_detail", pk=pk)


# Отмена публикации товара (только для модераторов)
class ProductUnpublishView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Отмена публикации продукта (только для модераторов)"""

    def test_func(self):
        """Проверяем, имеет ли пользователь право снимать с публикации"""
        return self.request.user.has_perm("catalog.can_unpublish_product")

    def post(self, request, pk):
        """Обрабатываем POST-запрос на снятие с публикации"""
        product = get_object_or_404(Product, pk=pk)
        product.is_published = False
        product.save()

        messages.success(request, f'Продукт "{product.name}" снят с публикации')
        return redirect("product_detail", pk=pk)


# Тестовая страница пагинации (FBV)
def test_pagination(request):
    """Тестовая страница для проверки пагинации"""
    products_list = Product.objects.all().order_by("-created_at")
    paginator = Paginator(products_list, 3)  # По 3 товара на страницу для теста
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "catalog/test_pagination.html",
        {
            "page_obj": page_obj,
        },
    )
