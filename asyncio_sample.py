import asyncio
from concurrent.futures import ThreadPoolExecutor
import time

# Функция, которую нужно выполнить асинхронно


def blocking_sleep(seconds):
    print(f"Sleeping for {seconds} seconds synchronously")
    time.sleep(seconds)
    print(f"Finished sleeping for {seconds} seconds")

# Асинхронная оболочка для синхронной функции


async def async_sleep(executor, seconds):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(executor, blocking_sleep, seconds)


async def main():
    # Создаем пул потоков
    with ThreadPoolExecutor() as executor:
        # Выполняем синхронную функцию асинхронно
        await asyncio.gather(
            async_sleep(executor, 3),
            async_sleep(executor, 3),
            async_sleep(executor, 3),
            async_sleep(executor, 3)
        )

# Запускаем асинхронную функцию
asyncio.run(main())
