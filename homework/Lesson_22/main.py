import threading


def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def check(number, results):
    results[number] = is_prime(number)


num_list = [17, 25, 74, 199, 101, 41, 39, 50, 20, 19, 51]

results = {}
threads = []

for number in num_list:
    t = threading.Thread(target=check, args=(number, results))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

for number in num_list:
    print(f"{number}: {'prime' if results[number] else 'not prime'}")