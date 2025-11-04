from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductForm
from .models import Contact, Product


def add_product(request):
    """Контроллер формы добавления товара"""
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("home")  # Перенаправляем на главную после успеха
    else:
        form = ProductForm()

    return render(request, "catalog/add_product.html", {"form": form})


def product_detail(request, pk):
    """Контроллер страницы одного товара"""
    product = get_object_or_404(Product, pk=pk)

    context = {
        "product": product,
    }
    return render(request, "catalog/product_detail.html", context)


def home(request):
    """Контроллер главной страницы с пагинацией"""
    # Получаем ВСЕ продукты и сортируем по дате создания
    all_products = Product.objects.all().order_by("-created_at")

    # Создаем пагинатор - 6 товаров на страницу
    paginator = Paginator(all_products, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Сокращаем описание для карточек
    for product in page_obj:
        if product.description and len(product.description) > 100:
            product.short_description = product.description[:100] + "..."
        else:
            product.short_description = product.description or "Описание отсутствует"

    context = {
        "page_obj": page_obj,  # 📍 МЕНЯЕМ latest_products на page_obj
    }
    return render(request, "catalog/home.html", context)


def contacts(request):
    """Контроллер страницы контактов"""
    contact_info = Contact.objects.first()  # Берем первую запись

    context = {
        "contact": contact_info,
    }
    return render(request, "catalog/contacts.html", context)
