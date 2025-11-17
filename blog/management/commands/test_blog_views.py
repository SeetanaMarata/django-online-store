from django.core.management.base import BaseCommand

from blog.models import BlogPost


class Command(BaseCommand):
    help = "Test blog views counting and email notifications"

    def handle(self, *args, **options):
        # Создаем тестовую статью с 99 просмотрами
        post, created = BlogPost.objects.get_or_create(
            title="Тестовая статья для проверки уведомлений",
            defaults={
                "content": "Это тестовая статья для проверки email уведомлений при достижении 100 просмотров.",
                "is_published": True,
                "views_count": 99,  # Почти у цели!
            },
        )

        if created:
            self.stdout.write(
                self.style.SUCCESS("✅ Создана тестовая статья с 99 просмотрами")
            )
            self.stdout.write(f"📝 Статья: {post.title}")
            self.stdout.write(f"👁️ Просмотров: {post.views_count}")
            self.stdout.write(
                "💡 Чтобы проверить уведомление, откройте статью один раз (просмотры достигнут 100)"
            )
        else:
            self.stdout.write(self.style.WARNING("ℹ️ Тестовая статья уже существует"))
