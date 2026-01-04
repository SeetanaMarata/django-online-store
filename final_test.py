import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "online_store.settings")
django.setup()

print("🎯 ФИНАЛЬНАЯ ПРОВЕРКА СИСТЕМЫ")
print("=" * 60)

from django.conf import settings
from django.contrib.auth import get_user_model

from catalog.models import Product

User = get_user_model()

# 1. Проверка настроек
print("\n1. НАСТРОЙКИ:")
print(f'   TEMPLATES DIRS: {settings.TEMPLATES[0]["DIRS"]}')
print(f"   BASE_DIR: {settings.BASE_DIR}")

# 2. Проверка пользователей
print("\n2. ПОЛЬЗОВАТЕЛИ:")
for email in ["admin@shop.com", "moderator@shop.com", "user@shop.com"]:
    try:
        user = User.objects.get(email=email)
        groups = [g.name for g in user.groups.all()]
        print(f"   ✅ {email}")
        print(f"      Активен: {user.is_active}")
        print(f'      Группы: {groups if groups else "нет"}')
    except User.DoesNotExist:
        print(f"   ❌ {email} - не найден")

# 3. Проверка модератора
print("\n3. ПРАВА МОДЕРАТОРА:")
moderator = User.objects.get(email="moderator@shop.com")
perms_to_check = [
    ("can_unpublish_product", "Отмена публикации"),
    ("delete_product", "Удаление товаров"),
    ("change_product", "Редактирование товаров"),
]

for perm_code, perm_name in perms_to_check:
    has_perm = moderator.has_perm(f"catalog.{perm_code}")
    status = "✅" if has_perm else "❌"
    print(f"   {status} {perm_name}: {has_perm}")

# 4. Проверка товаров
print("\n4. ТЕСТОВЫЕ ТОВАРЫ:")
products = Product.objects.all()
if products.exists():
    print(f"   ✅ Товаров в базе: {products.count()}")

    # Найдем товар созданный пользователем для теста
    user_product = Product.objects.filter(owner__email="user@shop.com").first()
    if user_product:
        print(f"   Тестовый товар пользователя:")
        print(f"      • {user_product.name}")
        print(f"        ID: {user_product.id}")
        print(f"        Владелец: {user_product.owner.email}")
        print(f"        Опубликован: {user_product.is_published}")
        print(f"        URL: /product/{user_product.id}/")
    else:
        print("   ℹ️ Создайте товар как user@shop.com для теста")
else:
    print("   ℹ️ Товаров нет")

print("\n" + "=" * 60)
print("📋 ИНСТРУКЦИЯ ДЛЯ ТЕСТИРОВАНИЯ:")
print("=" * 60)
print("1. Войди как user@shop.com (пароль: user123)")
print('2. Создай товар через "Создать товар" в меню')
print("3. Выйди и войди как moderator@shop.com (пароль: moder123)")
print("4. Перейди на страницу созданного товара")
print("5. Убедись что есть кнопки:")
print("   • Редактировать ✅")
print("   • Удалить ✅")
print("   • Снять с публикации ✅ (если товар опубликован)")
print("=" * 60)
