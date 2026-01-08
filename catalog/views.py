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
from django.core.cache import cache
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from .models import Product, Category, Contact
from .forms import ProductForm
from .services import (
    get_products_by_category,
    get_all_published_products,
    get_all_products_for_moderators
)


# Главная страница с пагинацией и кешированием
def home(request):
    """Главная страница с товарами и пагинацией"""
    cache_key = f'home_page_{request.GET.get("page", 1)}'
    cached_data = cache.get(cache_key)

    # Проверяем, если есть кеш и кеширование включено
    if cached_data and settings.CACHE_ENABLED:
        return cached_data

    # Новая версия: для обычных пользователей - опубликованные,
    # для модераторов и владельцев - все товары
    if request.user.is_authenticated and (
            request.user.has_perm("catalog.can_unpublish_product")
            or request.user.is_superuser
    ):
        # Модераторы видят ВСЕ товары
        products_list = get_all_products_for_moderators()
    else:
        # Обычные пользователи видят только опубликованные
        products_list = get_all_published_products()

    # Получаем все категории для боковой панели
    categories = Category.objects.all()

    # Пагинация - 6 товаров на страницу
    paginator = Paginator(products_list, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Формируем контекст
    context = {
        "page_obj": page_obj,
        "products": page_obj.object_list,
        "categories": categories,
        "cache_enabled": settings.CACHE_ENABLED,  # ← ДОБАВЬ ЭТУ СТРОЧКУ
        "cache_ttl": settings.CACHE_TTL,  # ← И ЭТУ
    }

    # Кешируем страницу, если включено кеширование
    if settings.CACHE_ENABLED:
        response = render(request, "catalog/home.html", context)
        cache.set(cache_key, response, settings.CACHE_TTL)
        return response

    return render(request, "catalog/home.html", context)


# Детальная страница товара с кешированием
class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    @method_decorator(cache_page(60 * 15 if settings.CACHE_ENABLED else 0))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()

        # Проверка прав на редактирование
        user = self.request.user
        context['can_edit'] = (
                user == product.owner or
                user.groups.filter(name='Модератор продуктов').exists() or
                user.is_superuser
        )

        return context


# Страница товаров по категории с кешированием
class CategoryProductsView(ListView):
    template_name = "catalog/category_products.html"
    context_object_name = "products"
    paginate_by = 6

    def get_queryset(self):
        category_slug = self.kwargs['slug']
        return get_products_by_category(category_slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs['slug']
        context['category'] = get_object_or_404(Category, slug=category_slug)
        return context


# Страница контактов (CBV)
class ContactsView(TemplateView):
    template_name = "catalog/contacts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contact_info = Contact.objects.first()
        context["contact"] = contact_info
        return context


# Создание товара (CBV)
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.is_published = False
        messages.success(self.request, "Товар успешно создан! Ожидает модерации.")

        # Очищаем кеш при создании нового продукта
        if settings.CACHE_ENABLED:
            cache.delete('all_published_products')
            cache.delete('all_products_moderators')
            cache.delete_pattern('*home_page*')

        return super().form_valid(form)


# Редактирование товара (CBV)
class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("home")

    def test_func(self):
        product = self.get_object()
        user = self.request.user
        return (
                product.owner == user
                or user.has_perm("catalog.can_unpublish_product")
                or user.is_superuser
        )

    def form_valid(self, form):
        messages.success(self.request, "Товар успешно обновлен!")

        # Очищаем кеш при обновлении продукта
        if settings.CACHE_ENABLED:
            product = self.get_object()
            cache.delete(f'products_category_{product.category.slug}')
            cache.delete('all_published_products')
            cache.delete('all_products_moderators')
            cache.delete_pattern(f'*product_detail_{product.id}*')
            cache.delete_pattern('*home_page*')

        return super().form_valid(form)


# Удаление товара (CBV)
class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("home")

    def test_func(self):
        product = self.get_object()
        user = self.request.user
        return (
                product.owner == user
                or user.has_perm("catalog.delete_product")
                or user.is_superuser
        )

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        category_slug = product.category.slug if product.category else None

        # Очищаем кеш перед удалением
        if settings.CACHE_ENABLED and category_slug:
            cache.delete(f'products_category_{category_slug}')
            cache.delete('all_published_products')
            cache.delete('all_products_moderators')
            cache.delete_pattern(f'*product_detail_{product.id}*')
            cache.delete_pattern('*home_page*')

        messages.success(request, "Товар успешно удален!")
        return super().delete(request, *args, **kwargs)


# Публикация товара
class ProductPublishView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Публикация продукта (только для модераторов)"""

    def test_func(self):
        return self.request.user.has_perm("catalog.can_unpublish_product")

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.is_published = True
        product.save()

        # Очищаем кеш
        if settings.CACHE_ENABLED:
            if product.category:
                cache.delete(f'products_category_{product.category.slug}')
            cache.delete('all_published_products')
            cache.delete('all_products_moderators')
            cache.delete_pattern(f'*product_detail_{product.id}*')
            cache.delete_pattern('*home_page*')

        messages.success(request, f'Продукт "{product.name}" опубликован')
        return redirect("product_detail", pk=pk)


# Отмена публикации товара
class ProductUnpublishView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Отмена публикации продукта (только для модераторов)"""

    def test_func(self):
        return self.request.user.has_perm("catalog.can_unpublish_product")

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.is_published = False
        product.save()

        # Очищаем кеш
        if settings.CACHE_ENABLED:
            if product.category:
                cache.delete(f'products_category_{product.category.slug}')
            cache.delete('all_published_products')
            cache.delete('all_products_moderators')
            cache.delete_pattern(f'*product_detail_{product.id}*')
            cache.delete_pattern('*home_page*')

        messages.success(request, f'Продукт "{product.name}" снят с публикации')
        return redirect("product_detail", pk=pk)


# Тестовая страница пагинации
def test_pagination(request):
    """Тестовая страница для проверки пагинации"""
    products_list = Product.objects.all().order_by("-created_at")
    paginator = Paginator(products_list, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "catalog/test_pagination.html",
        {
            "page_obj": page_obj,
        },
    )


from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render


@staff_member_required
def cache_stats(request):
    """Страница статистики кеша (только для staff)"""
    from django.core.cache import cache
    from django.conf import settings

    stats = {
        'cache_enabled': settings.CACHE_ENABLED,
        'cache_ttl': settings.CACHE_TTL,
        'cache_backend': settings.CACHES['default']['BACKEND'],
        'cache_timeout': settings.CACHES['default'].get('TIMEOUT', 'по умолчанию'),
    }

    # Попробуем получить размер кеша
    try:
        if hasattr(cache, '_cache'):
            if hasattr(cache._cache, '_cache'):
                stats['cache_size'] = len(cache._cache._cache)
            else:
                stats['cache_size'] = 'не удалось определить'
    except:
        stats['cache_size'] = 'ошибка при определении'

    # Тест работы кеша
    test_key = 'cache_stats_test'
    cache.set(test_key, 'test_value', 10)
    stats['cache_test'] = cache.get(test_key) == 'test_value'

    return render(request, 'catalog/cache_stats.html', {'stats': stats})