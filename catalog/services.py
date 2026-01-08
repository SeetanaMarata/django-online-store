from django.core.cache import cache
from django.conf import settings
from .models import Product, Category


def get_products_by_category(category_slug):
    """
    Сервисная функция для получения продуктов по категории
    с использованием кеширования
    """
    cache_key = f'products_category_{category_slug}'
    cached_data = cache.get(cache_key)

    if cached_data and settings.CACHE_ENABLED:
        return cached_data

    try:
        category = Category.objects.get(slug=category_slug)
        products = Product.objects.filter(
            category=category,
            is_published=True
        ).select_related('category', 'owner')

        if settings.CACHE_ENABLED:
            cache.set(cache_key, products, settings.CACHE_TTL)

        return products
    except Category.DoesNotExist:
        return Product.objects.none()


def get_all_published_products():
    """
    Сервисная функция для получения всех опубликованных продуктов
    с использованием кеширования
    """
    cache_key = 'all_published_products'
    cached_data = cache.get(cache_key)

    if cached_data and settings.CACHE_ENABLED:
        return cached_data

    products = Product.objects.filter(
        is_published=True
    ).select_related('category', 'owner').order_by('-created_at')

    if settings.CACHE_ENABLED:
        cache.set(cache_key, products, settings.CACHE_TTL)

    return products


def get_all_products_for_moderators():
    """
    Сервисная функция для модераторов (все продукты)
    """
    cache_key = 'all_products_moderators'
    cached_data = cache.get(cache_key)

    if cached_data and settings.CACHE_ENABLED:
        return cached_data

    products = Product.objects.all().select_related('category', 'owner').order_by('-created_at')

    if settings.CACHE_ENABLED:
        cache.set(cache_key, products, 60 * 5)  # 5 минут для модераторов

    return products