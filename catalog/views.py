from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView,
                                  TemplateView, UpdateView)

from .forms import ProductForm
from .models import Contact, Product


# ========== ГЛАВНАЯ СТРАНИЦА (ФУНКЦИЯ!) ==========
def home(request):
    """Главная страница с товарами и пагинацией"""
    # Получаем ВСЕ товары, сортируем по дате (новые сначала)
    all_products = Product.objects.all().order_by("-created_at")

    # Создаем пагинатор: 6 товаров на страницу
    paginator = Paginator(all_products, 6)

    # Получаем номер страницы из GET-параметра
    page_number = request.GET.get("page")

    try:
        # Получаем объект страницы
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        # Если page не число, показываем первую страницу
        page_obj = paginator.page(1)
    except EmptyPage:
        # Если страница вне диапазона, показываем последнюю
        page_obj = paginator.page(paginator.num_pages)

    # Добавляем короткое описание для каждого товара
    for product in page_obj:
        if product.description and len(product.description) > 100:
            product.short_description = product.description[:100] + "..."
        else:
            product.short_description = product.description or "Описание отсутствует"

    # Подготавливаем контекст
    context = {
        "page_obj": page_obj,
        "products": page_obj,  # дублируем для совместимости
    }

    return render(request, "catalog/home.html", context)


# ========== СТРАНИЦА ТОВАРА (CBV) ==========
class ProductDetailView(DetailView):
    """Страница одного товара"""

    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


# ========== СТРАНИЦА КОНТАКТОВ (CBV) ==========
class ContactsView(TemplateView):
    """Страница контактов"""

    template_name = "catalog/contacts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["contact"] = Contact.objects.first()
        return context


# ========== СОЗДАНИЕ ТОВАРА (CBV) ==========
class ProductCreateView(
    LoginRequiredMixin, CreateView
):  # 📍 LoginRequiredMixin ПЕРВЫЙ!
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("home")
    login_url = "/users/login/"  # 📍 Важно указать куда перенаправлять


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    login_url = "/users/login/"

    def get_success_url(self):
        return reverse_lazy("product_detail", kwargs={"pk": self.object.pk})


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("home")
    login_url = "/users/login/"


# ========== ТЕСТОВАЯ СТРАНИЦА ПАГИНАЦИИ ==========
def test_pagination(request):
    """Тестовая страница для отладки пагинации"""
    all_products = Product.objects.all().order_by("-created_at")
    paginator = Paginator(all_products, 6)
    page_number = request.GET.get("page", 1)

    try:
        page_obj = paginator.page(page_number)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.page(1)

    return render(request, "catalog/test_pagination.html", {"page_obj": page_obj})
