import asyncio
import time

tasks = [
    ("Downloading data", 3),
    ("Processing data", 2),
    ("Sending notification", 1),
    ("Saving results", 4),
]


async def do_task(name, duration):
    print(f"{name} started.")

    await asyncio.sleep(duration)

    print(f"{name} finished.")

    return f"{name} completed"


async def run_sequential():
    results = []

    start = time.perf_counter()

    for name, duration in tasks:
        result = await do_task(name, duration)
        results.append(result)

    end = time.perf_counter()

    print("\nSequential Results:")
    for result in results:
        print(result)

    return end - start


async def run_concurrent():
    start = time.perf_counter()

    coroutines = [
        do_task(name, duration)
        for name, duration in tasks
    ]

    results = await asyncio.gather(*coroutines)

    end = time.perf_counter()

    print("\nConcurrent Results:")
    for result in results:
        print(result)

    return end - start


async def main():
    print("=== Sequential Execution ===")
    sequential_time = await run_sequential()

    print("\n=== Concurrent Execution ===")
    concurrent_time = await run_concurrent()

    print("\nComparison")
    print(f"Sequential execution time: {sequential_time:.2f} seconds")
    print(f"Concurrent execution time: {concurrent_time:.2f} seconds")


if __name__ == "__main__":
    asyncio.run(main())