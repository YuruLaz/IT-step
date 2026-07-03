def tax(func):
    def wrapper(balance, amount):
        fee = 1
        if balance < amount + fee:
            print("ანგარიშზე საკმარისი თანხა არ არის!")
        else:
            return func(balance, amount + fee)

    return wrapper


@tax
def trans(balance, amount):
    balance -= amount
    print(f"ტრანზაქცია წარმატებით შესრულდა.")
    print(f"დარჩენილი ბალანსი: {balance} ლარი")


trans(100, 20)

