from django.core.management import call_command
from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Load test data for products and categories"

    def handle(self, *args, **options):
        # Удаляем существующие данные
        self.stdout.write("🗑️  Удаляем старые данные...")
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Загружаем данные из фикстур
        self.stdout.write("📥 Загружаем тестовые данные...")

        try:
            # Указываем кодировку явно для Windows
            call_command("loaddata", "category_data.json", verbosity=0)
            call_command("loaddata", "product_data.json", verbosity=0)

            self.stdout.write(
                self.style.SUCCESS("✅ Тестовые данные успешно загружены!")
            )

            # Покажем сколько данных загрузилось
            categories_count = Category.objects.count()
            products_count = Product.objects.count()
            self.stdout.write(
                f"📊 Загружено: {categories_count} категорий, {products_count} продуктов"
            )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Ошибка при загрузке данных: {e}"))
            self.stdout.write("💡 Попробуй пересоздать фикстуры командой:")
            self.stdout.write(
                "python manage.py dumpdata catalog.Category --indent 2 > catalog/fixtures/category_data.json"
            )
