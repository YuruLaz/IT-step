choice = int(input("ამოირჩიეთ ამოცანა (1, 2, 3):"))
if choice == 1:
    dict_comph = {i:i**2 for i in range(1, 11)}
    print(dict_comph) 

elif choice == 2:
    products = [
        {"cola": {
            "price": 1.5,
            "quantity": 10
        }},
        {"fanta": {
            "price": 2.5,
            "quantity": 5
        }},
        {"snickers": {
            "price": 3.5,
            "quantity": 12
        }},
        {"water": {
            "price": 4.5,
            "quantity": 8
        }},
        {"beer": {
            "price": 6.5,
            "quantity": 5
        }}
    ]

    #ა
    for product in products:
        print(list(product.keys())[0])

    #ბ
    sum_ = 0
    for product in products:
        for values in product.values():
            sum_ += values['price']*values['quantity']
    print(sum_)

elif choice == 3:
    fruit_count = {}
    while True:
        fruit = input("Enter your favorite fruit (or 'stop'): ")

        if fruit == 'stop':
            break

        fruit_count[fruit] = fruit_count.get(fruit, 0) + 1

    print(fruit_count)