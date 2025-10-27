from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    """Контроллер главной страницы"""
    return render(request, "catalog/home.html")


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
