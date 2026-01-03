import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "online_store.settings")
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

print("🔄 СОЗДАНИЕ ТЕСТОВЫХ ПОЛЬЗОВАТЕЛЕЙ")
print("=" * 50)

User = get_user_model()

# 1. Обновляем суперпользователя
admin_email = "admin@shop.com"
try:
    admin = User.objects.get(email=admin_email)
    admin.is_staff = True
    admin.is_superuser = True
    admin.set_password("admin123")
    admin.save()
    print(f"✅ Админ {admin_email} обновлен")
except User.DoesNotExist:
    admin = User.objects.create_superuser(
        email=admin_email, username="admin", password="admin123"
    )
    print(f"✅ Админ {admin_email} создан")

# 2. Получаем группы
try:
    moderator_group = Group.objects.get(name="Модератор продуктов")
    content_group = Group.objects.get(name="Контент-менеджер")
    print("✅ Группы найдены")
except Group.DoesNotExist:
    print("❌ Группы не найдены!")
    exit()

# 3. Создаем или получаем модератора
moderator_email = "moderator@shop.com"
try:
    moderator = User.objects.get(email=moderator_email)
    print(f"ℹ️ Модератор {moderator_email} уже существует")
except User.DoesNotExist:
    # Создаем с уникальным username
    moderator = User.objects.create_user(
        email=moderator_email,
        username="moderator_user",  # Уникальное имя
        password="moder123",
        is_staff=True,
    )
    print(f"✅ Модератор {moderator_email} создан")

# Обновляем пароль и добавляем в группу
moderator.set_password("moder123")
moderator.is_staff = True
moderator.groups.add(moderator_group)
moderator.save()

# 4. Создаем обычного пользователя
user_email = "user@shop.com"
try:
    user = User.objects.get(email=user_email)
    print(f"ℹ️ Пользователь {user_email} уже существует")
except User.DoesNotExist:
    user = User.objects.create_user(
        email=user_email,
        username="regular_user",  # Уникальное имя
        password="user123",
        is_staff=False,
    )
    print(f"✅ Пользователь {user_email} создан")

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

# Показываем текущих пользователей
print("\n📊 ТЕКУЩИЕ ПОЛЬЗОВАТЕЛИ:")
for user in User.objects.all():
    groups = [g.name for g in user.groups.all()]
    print(f"• {user.email} (staff: {user.is_staff})")
    if groups:
        print(f'  Группы: {", ".join(groups)}')
