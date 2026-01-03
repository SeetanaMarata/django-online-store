import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "online_store.settings")
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from catalog.models import Product

User = get_user_model()

print("ПОЛНАЯ ПРОВЕРКА СИСТЕМЫ")
print("=" * 60)

# 1. Группы
print("\n1. ГРУППЫ:")
groups = list(Group.objects.all())
if groups:
    for group in groups:
        print(f"   ✅ {group.name}")
else:
    print("   ❌ Группы не найдены")

# 2. Ключевые пользователи
print("\n2. ПОЛЬЗОВАТЕЛИ:")
test_users = ["admin@shop.com", "moderator@shop.com", "user@shop.com"]
all_ok = True

for email in test_users:
    try:
        user = User.objects.get(email=email)
        groups = [g.name for g in user.groups.all()]
        status = "✅" if user.is_active else "❌"
        print(f"   {status} {email}")
        print(f"      Активен: {user.is_active}")
        print(f"      Персонал: {user.is_staff}")
        if groups:
            print(f'      Группы: {", ".join(groups)}')

        if email == "moderator@shop.com":
            has_perm = user.has_perm("catalog.can_unpublish_product")
            print(f"      Право отмены публикации: {has_perm}")

    except User.DoesNotExist:
        print(f"   ❌ {email} - не найден")
        all_ok = False

# 3. Товары
print("\n3. ТОВАРЫ:")
products_count = Product.objects.count()
if products_count > 0:
    print(f"   ✅ Товаров в базе: {products_count}")
    # Покажем товары с владельцами
    for product in Product.objects.all()[:3]:
        owner = product.owner.email if product.owner else "не указан"
        print(f"      • {product.name}")
        print(f"        Владелец: {owner}")
        print(f"        Опубликован: {product.is_published}")
else:
    print("   ℹ️ Товаров нет")

print("\n" + "=" * 60)
print("РЕЗУЛЬТАТ:")
print("=" * 60)

if all_ok and len(groups) >= 2:
    print("✅ СИСТЕМА НАСТРОЕНА ПРАВИЛЬНО!")
    print("Теперь можно тестировать функционал модерации.")
else:
    print("⚠️ Есть проблемы. Проверь:")
    if len(groups) < 2:
        print("   • Группы созданы? Запусти: python manage.py create_groups")
    if not all_ok:
        print("   • Все пользователи созданы?")
