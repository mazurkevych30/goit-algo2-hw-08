import random
import time

from make_queries import make_queries
from LRU_cache import LRUCache


def range_sum_no_cache(array, left, right):
    return sum(array[left : right + 1])


def update_no_cache(array, index, value):
    array[index] = value


def range_sum_with_cache(array, left, right, cache: LRUCache):
    total = cache.get((left, right))
    if total != -1:
        return total
    total = sum(array[left : right + 1])
    cache.put((left, right), total)
    return total


def update_with_cache(array, index, value, cache: LRUCache):
    array[index] = value
    for key in list(cache.cache.keys()):
        left, right = key
        if left <= index <= right:
            cache.delete(key)


requests = make_queries(100_000, 50_000)

N = 100_000
numbers = [random.randint(1, 100) for _ in range(N)]

start_no_cache = time.time()
for type_req, L, R in requests:
    if type_req == "Range":
        range_sum_no_cache(numbers, L, R)
    else:
        update_no_cache(numbers, L, R)
finish_no_cache = time.time() - start_no_cache

my_cache = LRUCache(1000)

start_with_cache = time.time()
for type_req, L, R in requests:
    if type_req == "Range":
        range_sum_with_cache(numbers, L, R, my_cache)
    else:
        update_with_cache(numbers, L, R, my_cache)
finish_with_cache = time.time() - start_with_cache

speedup = finish_no_cache / finish_with_cache

print(f"Без кешу : {finish_no_cache:.2f} c")
print(f"LRU-кеш  : {finish_with_cache:.2f} c  (прискорення ×{speedup:.2f})")
