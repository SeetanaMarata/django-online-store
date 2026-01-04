import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "online_store.settings")
django.setup()

from django.template.loader import get_template

print("🔍 ПРОВЕРКА ШАБЛОНОВ")
print("=" * 50)

templates_to_check = [
    "base.html",
    "catalog/home.html",
    "catalog/product_detail.html",
    "users/login.html",
    "users/profile.html",
]

for template_name in templates_to_check:
    try:
        template = get_template(template_name)
        print(f"✅ {template_name} - найден")
    except Exception as e:
        print(f"❌ {template_name} - ОШИБКА: {e}")

print("\n" + "=" * 50)
print("Если base.html не найден, проверь TEMPLATES в settings.py")
print('Убедись что есть строка: DIRS: [BASE_DIR / "templates"]')
