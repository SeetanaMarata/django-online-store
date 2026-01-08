import time
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_store.settings')
django.setup()

from catalog.services import get_all_published_products

print("Тест кеширования сервисных функций...")
print("=" * 50)

# Первый вызов - должен загрузить из базы
start = time.time()
products1 = get_all_published_products()
time1 = time.time() - start
print(f"Первый вызов: {time1:.4f} сек, {len(products1)} продуктов")

# Второй вызов - должен взять из кеша
start = time.time()
products2 = get_all_published_products()
time2 = time.time() - start
print(f"Второй вызов: {time2:.4f} сек, {len(products2)} продуктов")

if time2 < time1:
    print("✅ Кеширование работает! Второй вызов быстрее.")
else:
    print("⚠️ Кеширование может не работать.")

print("=" * 50)