import time

import requests

print("Тест кеширования страницы продукта...")
print("=" * 50)

# URL твоего продукта (замени на реальный)
url = "http://127.0.0.1:8000/product/1/"

# Первый запрос
print("Первый запрос (должен быть медленнее)...")
start = time.time()
response1 = requests.get(url)
time1 = time.time() - start
print(f"Время: {time1:.4f} сек")
print(f"Статус: {response1.status_code}")

# Второй запрос (должен быть быстрее из кеша)
print("\nВторой запрос (должен быть быстрее)...")
start = time.time()
response2 = requests.get(url)
time2 = time.time() - start
print(f"Время: {time2:.4f} сек")
print(f"Статус: {response2.status_code}")

if time2 < time1:
    print(f"\n✅ Кеширование страницы работает! Ускорение: {time1/time2:.1f}x")
else:
    print("\n⚠️ Кеширование страницы может не работать")

print("=" * 50)
