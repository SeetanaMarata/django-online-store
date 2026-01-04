import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "online_store.settings")
django.setup()

from django.contrib.auth import get_user_model

from catalog.models import Category, Product

User = get_user_model()

print("🔍 ПРОВЕРКА ПРАВ МОДЕРАТОРА")
print("=" * 50)

# Находим модератора
try:
    moderator = User.objects.get(email="moderator@shop.com")
    print(f"✅ Найден модератор: {moderator.email}")

    # Проверяем права
    print("\n📋 Права модератора:")
    print(
        f'• can_unpublish_product: {moderator.has_perm("catalog.can_unpublish_product")}'
    )
    print(f'• delete_product: {moderator.has_perm("catalog.delete_product")}')
    print(f'• change_product: {moderator.has_perm("catalog.change_product")}')
    print(f'• add_product: {moderator.has_perm("catalog.add_product")}')

    # Проверяем группы
    print("\n👥 Группы модератора:")
    for group in moderator.groups.all():
        print(f"• {group.name}")
        for perm in group.permissions.all():
            print(f"  - {perm.codename}")

except User.DoesNotExist:
    print("❌ Модератор не найден!")
    print("Запусти: python create_users_fixed.py")

# Создаем тестовый товар если нет
print("\n🛒 Тестовые товары:")
if Product.objects.count() == 0:
    category, _ = Category.objects.get_or_create(
        name="Тестовая категория", defaults={"description": "Для тестирования"}
    )

    # Создаем от имени обычного пользователя
    try:
        user = User.objects.get(email="user@shop.com")
        product = Product.objects.create(
            name="Тестовый товар",
            description="Этот товар создан для проверки прав модератора",
            price=1000,
            category=category,
            owner=user,
            is_published=True,
        )
        print(f"✅ Создан тестовый товар: {product.name}")
        print(f"   Владелец: {product.owner.email}")
    except User.DoesNotExist:
        print("❌ Обычный пользователь не найден")
else:
    for product in Product.objects.all()[:3]:
        print(
            f'• {product.name} (владелец: {product.owner.email if product.owner else "нет"})'
        )
