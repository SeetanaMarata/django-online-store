from django.shortcuts import render

from .models import Product


def home(request):
    """Контроллер главной страницы"""
    # Получаем последние 5 продуктов
    latest_products = Product.objects.all().order_by("-created_at")[:5]

    # Выводим в консоль (для проверки)
    print("🎯 Последние 5 продуктов:")
    for product in latest_products:
        print(f"  - {product.name} ({product.price} руб.)")

    context = {
        "latest_products": latest_products,
    }
    return render(request, "catalog/home.html", context)


def contacts(request):
    """Контроллер страницы контактов"""
    if request.method == "POST":
        # Обработка формы (пока просто сообщение)
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        print(f"Новое сообщение от {name}, телефон: {phone}, сообщение: {message}")
        return render(request, "catalog/contacts.html", {"success": True})

    return render(request, "catalog/contacts.html")
