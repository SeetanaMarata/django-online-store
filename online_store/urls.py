from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("catalog.urls")),  # 📍 ПОДКЛЮЧАЕМ ПРИЛОЖЕНИЕ CATALOG
]
