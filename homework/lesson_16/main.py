from bank_brain import bank

count = 1

accounts = {}
acc_num = f"acc{count}" 

print("\n========BANK========")
print("1. Add a new account")
print("2. Login into an existing account")

choice = input("\nChoose 1, 2 or 3: ")

while True:

    if choice == "1":
        name = input("input your name and surname: ")
        money = int(input("input your balance: "))

        account = bank(owner=name, balance=money)
        accounts[acc_num] = account.get_account_number()
        count += 1

        account



        