from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Create test products for development"

    def handle(self, *args, **options):
        # Создаем категории
        electronics, _ = Category.objects.get_or_create(
            name="Electronics", defaults={"description": "Tech gadgets"}
        )

        books, _ = Category.objects.get_or_create(
            name="Books", defaults={"description": "Literature"}
        )

        # Создаем товары
        products = [
            {
                "name": "iPhone 15 Pro",
                "description": "Flagship smartphone from Apple",
                "price": 99999.99,
                "category": electronics,
            },
            {
                "name": "MacBook Air",
                "description": "Light and powerful laptop",
                "price": 129999.99,
                "category": electronics,
            },
            {
                "name": "War and Peace",
                "description": "Novel by Leo Tolstoy",
                "price": 1500.00,
                "category": books,
            },
        ]

        for product_data in products:
            product, created = Product.objects.get_or_create(
                name=product_data["name"], defaults=product_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Created product: {product.name}")
                )

        self.stdout.write(self.style.SUCCESS("Test products created successfully!"))
