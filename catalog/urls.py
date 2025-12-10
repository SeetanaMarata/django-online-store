from django.urls import path

from . import views  # Импортируем ВСЕ функции из views

urlpatterns = [
    # Главная страница - используем ФУНКЦИЮ views.home
    path("", views.home, name="home"),
    # Контакты
    path("contacts/", views.ContactsView.as_view(), name="contacts"),
    # Товары - CRUD
    path("product/<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("product/create/", views.ProductCreateView.as_view(), name="product_create"),
    path(
        "product/<int:pk>/edit/", views.ProductUpdateView.as_view(), name="product_edit"
    ),
    path(
        "product/<int:pk>/delete/",
        views.ProductDeleteView.as_view(),
        name="product_delete",
    ),
    # Тестовая страница пагинации
    path("test-pagination/", views.test_pagination, name="test_pagination"),
]
