from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from .forms import ProductForm
from .models import Contact, Product


class HomeView(ListView):
    """CBV для главной страницы с товарами"""

    model = Product
    template_name = "catalog/home.html"
    context_object_name = "page_obj"
    paginate_by = 6

    def get_queryset(self):
        return Product.objects.all().order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Сокращаем описание для карточек
        for product in context["page_obj"]:
            if product.description and len(product.description) > 100:
                product.short_description = product.description[:100] + "..."
            else:
                product.short_description = (
                    product.description or "Описание отсутствует"
                )

        return context


class ProductDetailView(DetailView):
    """CBV для страницы одного товара"""

    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


class ContactsView(TemplateView):
    """CBV для страницы контактов"""

    template_name = "catalog/contacts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["contact"] = Contact.objects.first()
        return context


class ProductCreateView(CreateView):
    """CBV для формы добавления товара"""

    model = Product
    form_class = ProductForm
    template_name = "catalog/add_product.html"
    success_url = reverse_lazy("home")
