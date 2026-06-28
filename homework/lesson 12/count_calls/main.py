def count_calls(func):
    count = 0
    def wrapper(*args, **kwargs):
        nonlocal count
        count += 1
        print(f"{func.__name__} არი გამოძახებული {count}-ჯერ")
        return func(*args, **kwargs)
    return wrapper


@count_calls
def add(a, b):
    return a + b

print(add(2, 5))
print(add(5, 10))
print(add(46, 3))