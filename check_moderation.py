import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "online_store.settings")
django.setup()

print("ПРОВЕРКА ПРАВ МОДЕРАТОРА")
print("=" * 50)

from django.contrib.auth import get_user_model

from catalog.models import Category, Product

User = get_user_model()

# 1. Находим модератора
moderator = User.objects.get(email="moderator@shop.com")
print(f"1. Найден модератор: {moderator.email}")

# 2. Проверяем права
print("\n2. Права модератора:")
print(
    f'   • can_unpublish_product: {moderator.has_perm("catalog.can_unpublish_product")}'
)
print(f'   • delete_product: {moderator.has_perm("catalog.delete_product")}')
print(f'   • change_product: {moderator.has_perm("catalog.change_product")}')

# 3. Проверяем группы
print("\n3. Группы модератора:")
for group in moderator.groups.all():
    print(f"   • {group.name}")

# 4. Создаем тестовый товар если нет
print("\n4. Тестовые данные:")
if Product.objects.count() == 0:
    category, _ = Category.objects.get_or_create(
        name="Тестовая категория", defaults={"description": "Для тестирования"}
    )

    user = User.objects.get(email="user@shop.com")
    product = Product.objects.create(
        name="Тестовый товар для модерации",
        description="Этот товар создан обычным пользователем",
        price=1500,
        category=category,
        owner=user,
        is_published=True,
    )
    print(f"   ✅ Создан тестовый товар")
    print(f"      Название: {product.name}")
    print(f"      Владелец: {product.owner.email}")
else:
    print(f"   ✅ Товаров в базе: {Product.objects.count()}")
    for product in Product.objects.all()[:3]:
        owner = product.owner.email if product.owner else "нет"
        print(f"      • {product.name} (владелец: {owner})")

print("\n" + "=" * 50)
print("ДЛЯ ТЕСТИРОВАНИЯ:")
print("=" * 50)
print("1. Войди на сайт как user@shop.com / user123")
print("2. Создай товар через форму /product/create/")
print("3. Выйди и войди как moderator@shop.com / moder123")
print("4. Зайди на страницу созданного товара")
print("5. Проверь что видишь кнопки:")
print("   • Редактировать (должна быть)")
print("   • Удалить (должна быть)")
print("   • Снять с публикации (если товар опубликован)")
