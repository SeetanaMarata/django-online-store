import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "online_store.settings")
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

print("🔄 СОЗДАНИЕ ТЕСТОВЫХ ПОЛЬЗОВАТЕЛЕЙ")
print("=" * 50)

User = get_user_model()

# 1. Создаем/обновляем суперпользователя
admin_email = "admin@shop.com"
admin, created = User.objects.get_or_create(
    email=admin_email,
    defaults={
        "username": "admin",
        "is_superuser": True,
        "is_staff": True,
        "is_active": True,
    },
)

if not admin.is_staff or not admin.is_superuser:
    admin.is_staff = True
    admin.is_superuser = True
    admin.save()
    print(f"✅ Админ {admin_email} обновлен")
elif created:
    print(f"✅ Админ {admin_email} создан")
else:
    print(f"ℹ️ Админ {admin_email} уже существует")

# Устанавливаем пароль
admin.set_password("admin123")
admin.save()

# 2. Получаем группы
try:
    moderator_group = Group.objects.get(name="Модератор продуктов")
    content_group = Group.objects.get(name="Контент-менеджер")
    print("✅ Группы найдены")
except Group.DoesNotExist:
    print("❌ Группы не найдены! Выполни: python manage.py create_groups")

# 3. Создаем модератора
moderator_email = "moderator@shop.com"
moderator, created = User.objects.get_or_create(
    email=moderator_email,
    defaults={"username": "moderator", "is_staff": True, "is_active": True},
)

if created:
    print(f"✅ Модератор {moderator_email} создан")
else:
    print(f"ℹ️ Модератор {moderator_email} уже существует")

# Устанавливаем пароль и группу
moderator.set_password("moder123")
if "moderator_group" in locals():
    moderator.groups.add(moderator_group)
moderator.save()

# 4. Создаем обычного пользователя
user_email = "user@shop.com"
user, created = User.objects.get_or_create(
    email=user_email,
    defaults={"username": "user", "is_staff": False, "is_active": True},
)

if created:
    print(f"✅ Пользователь {user_email} создан")
else:
    print(f"ℹ️ Пользователь {user_email} уже существует")

user.set_password("user123")
user.save()

print("\n" + "=" * 50)
print("📋 ГОТОВЫЕ ДАННЫЕ ДЛЯ ВХОДА:")
print("=" * 50)
print("1. АДМИН (видит ВСЕ в админке):")
print("   • Email: admin@shop.com")
print("   • Пароль: admin123")
print()
print("2. МОДЕРАТОР (управляет товарами):")
print("   • Email: moderator@shop.com")
print("   • Пароль: moder123")
print()
print("3. ПОЛЬЗОВАТЕЛЬ (обычный):")
print("   • Email: user@shop.com")
print("   • Пароль: user123")
print("=" * 50)
