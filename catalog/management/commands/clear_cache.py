from django.core.cache import cache
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Очистка всего кеша"

    def handle(self, *args, **options):
        cache.clear()
        self.stdout.write(self.style.SUCCESS("Кеш успешно очищен"))
