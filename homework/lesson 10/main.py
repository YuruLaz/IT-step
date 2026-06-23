#fruit_count[fruit] = fruit_count.get(fruit, 0) + 1

choice = int(input("ამოირჩიეთ ამოცანა (1, 2, 3, 4, 5):"))
if choice == 1:

    def sum_numbers(count=5):
        total = 0
        for _ in range(count):
            total += int(input("შეიყვანეთ რიცხვი: "))
        return total

    raw = input("შეიყვანეთ რამდენჯერ რავაჯამოთ: ")
    sum_counter = int(raw) if raw.strip() else 5
    print(sum_numbers(sum_counter))
    

elif choice == 2:

    def two_lists(*args):
        return list(filter(lambda i: not i % 2, args)), list(filter(lambda i: i % 2, args))
    print(two_lists(1,2,3,5,7,8,4,6,7,3,10))


elif choice == 3:
    
    def word_count(sentence):
        words = sentence.lower().split()
        counts = {}
        for word in words:
            word = word.strip(".,!?;:")
            counts[word] = counts.get(word, 0) + 1
        return counts

    sentence = input("შეიყვანეთ წინადადება: ")
    print(word_count(sentence))


elif choice == 4:

    from functools import reduce

    products = [
    {"name": "Laptop", "price": 1200},
    {"name": "Mouse", "price": 15},
    {"name": "Keyboard", "price": 25},
    {"name": "Monitor", "price": 150},
    {"name": "Power", "price": 100},
    {"name": "Pad", "price": 10},
    ]

    using_filter = list(filter(lambda i: i["price"] < 100, products))
    using_map = list(map(lambda i: (i["name"], i["price"]), products))
    using_sorted = list(sorted(products, key=lambda i: i["price"]))
    using_reduced = reduce(lambda a, b: a + b["price"], products, 0)

    print(f"fiter - {using_filter}")
    print(f"map - {using_map}")
    print(f"sorted - {using_sorted}")
    print(f"reduced - {using_reduced}")


elif choice == 5:
    def recursive(n):
        if n <= 0:
            return 0
        return n + recursive(n - 1)

    numbr = int(input("შეიყვანეთ რიცხვი: "))
    print(recursive(numbr))