from django.urls import path

from .views import ContactsView, HomeView, ProductCreateView, ProductDetailView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path(
        "add-product/", ProductCreateView.as_view(), name="add_product"
    ),  # 📍 ИМЯ: add_product
]
