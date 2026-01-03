from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from blog.models import BlogPost
from catalog.models import Product


class Command(BaseCommand):
    help = "Создает группы модераторов и контент-менеджеров"

    def handle(self, *args, **options):
        # Группа "Модератор продуктов"
        moderator_group, created = Group.objects.get_or_create(
            name="Модератор продуктов"
        )

        # Получаем разрешения для модели Product
        product_content_type = ContentType.objects.get_for_model(Product)
        product_permissions = Permission.objects.filter(
            content_type=product_content_type
        )

        # Добавляем все разрешения для продуктов + кастомные
        for perm in product_permissions:
            moderator_group.permissions.add(perm)

        # Добавляем кастомное разрешение на отмену публикации
        unpublish_perm, _ = Permission.objects.get_or_create(
            codename="can_unpublish_product",
            content_type=product_content_type,
            defaults={"name": "Может отменять публикацию продукта"},
        )
        moderator_group.permissions.add(unpublish_perm)

        # Группа "Контент-менеджер"
        content_manager_group, created = Group.objects.get_or_create(
            name="Контент-менеджер"
        )

        # Получаем разрешения для модели BlogPost
        blog_content_type = ContentType.objects.get_for_model(BlogPost)
        blog_permissions = Permission.objects.filter(content_type=blog_content_type)

        for perm in blog_permissions:
            content_manager_group.permissions.add(perm)

        self.stdout.write(self.style.SUCCESS("✅ Группы успешно созданы и настроены!"))
        self.stdout.write("📋 Список групп:")
        self.stdout.write("   • Модератор продуктов - может управлять товарами")
        self.stdout.write("   • Контент-менеджер - может управлять блогом")
