from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Create test data directly in database"

    def handle(self, *args, **options):
        # Удаляем существующие данные
        self.stdout.write("🗑️  Удаляем старые данные...")
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Создаем категории
        self.stdout.write("📝 Создаем категории...")
        electronics = Category.objects.create(
            name="Электроника", description="Техника и гаджеты"
        )
        books = Category.objects.create(
            name="Книги", description="Художественная и учебная литература"
        )
        clothing = Category.objects.create(
            name="Одежда", description="Модная одежда и аксессуары"
        )

        # Создаем продукты
        self.stdout.write("📦 Создаем продукты...")
        Product.objects.create(
            name="iPhone 15",
            description="Новый смартфон от Apple",
            price=89999.99,
            category=electronics,
        )
        Product.objects.create(
            name="MacBook Pro",
            description="Мощный ноутбук для работы",
            price=149999.99,
            category=electronics,
        )
        Product.objects.create(
            name="Война и мир",
            description="Роман Льва Толстого",
            price=1500.00,
            category=books,
        )
        Product.objects.create(
            name="Футболка хлопковая",
            description="Удобная футболка из 100% хлопка",
            price=1999.99,
            category=clothing,
        )

        self.stdout.write(self.style.SUCCESS("✅ Тестовые данные созданы успешно!"))
        self.stdout.write(
            f"📊 Создано: {Category.objects.count()} категорий, {Product.objects.count()} продуктов"
        )
