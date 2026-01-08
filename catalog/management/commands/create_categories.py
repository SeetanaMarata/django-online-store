from django.core.management.base import BaseCommand
from catalog.models import Category
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Создает или обновляет slug для существующих категорий'

    def handle(self, *args, **options):
        categories = Category.objects.all()

        for category in categories:
            if not category.slug:
                category.slug = slugify(category.name)
                category.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Создан slug для категории: {category.name}')
                )

        self.stdout.write(
            self.style.SUCCESS('Все категории обновлены со slug!')
        )