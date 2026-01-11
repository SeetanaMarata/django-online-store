import os
import sys

import django

# Настройка Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "online_store.settings")
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.conf import settings
from django.core.cache import cache

print("=" * 60)
print("Проверка подключения Django к Redis")
print("=" * 60)

print(f"REDIS_URL: {getattr(settings, 'REDIS_URL', 'Не настроен')}")
print(f"CACHE_ENABLED: {getattr(settings, 'CACHE_ENABLED', False)}")
print(f"CACHE_BACKEND: {settings.CACHES['default']['BACKEND']}")

try:
    # Тест 1: Запись в кеш
    print("\n1. Пробуем записать в кеш...")
    cache.set("test_key", "Hello Redis!", 30)
    print("   ✅ Запись успешна")

    # Тест 2: Чтение из кеша
    print("2. Пробуем прочитать из кеша...")
    value = cache.get("test_key")
    print(f"   ✅ Чтение успешно: {value}")

    # Тест 3: Проверка TTL
    print("3. Проверяем TTL...")
    import time

    cache.set("ttl_test", "value", 2)
    time.sleep(1)
    print(f"   После 1 секунды: {cache.get('ttl_test')}")
    time.sleep(2)
    print(f"   После 3 секунд: {cache.get('ttl_test')} (должен быть None)")

    # Тест 4: Сложные данные
    print("4. Тест сложных данных...")
    test_data = {
        "name": "Тестовый товар",
        "price": 1000,
        "category": "Электроника",
        "tags": ["новинка", "акция"],
    }
    cache.set("complex_data", test_data, 10)
    retrieved = cache.get("complex_data")
    print(f"   ✅ Сложные данные сохранены: {retrieved}")

    print("\n" + "=" * 60)
    print("🎉 ВСЁ РАБОТАЕТ! Redis подключен корректно!")
    print("=" * 60)

except Exception as e:
    print(f"\n❌ ОШИБКА: {e}")
    print("\nВозможные проблемы и решения:")
    print("1. Redis не запущен - проверь 'redis-server' или службы Windows")
    print("2. Неправильный порт - проверь .env файл (PORT=6379)")
    print("3. Брандмауэр блокирует - добавь исключение для порта 6379")
    print("4. Попробуй использовать '127.0.0.1' вместо 'localhost'")
