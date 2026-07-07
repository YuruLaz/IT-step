from bank_brain import Bank

accounts = {}


def read_amount(prompt):
    """Ask until the user types a valid non-negative whole number."""
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if value < 0:
            print("Amount cannot be negative.")
            continue

        return value


while True:
    print("\n========== BANK ==========")
    print("1. Add a new account")
    print("2. Login into an existing account")
    print("3. Exit")

    choice = input("Choose: ")

    if choice == "1":
        name = input("Enter owner's name: ")
        balance = read_amount("Enter starting balance: ")

        account = Bank(name, balance)
        account_number = account.get_account_number()

        # Store the actual object so we can operate on it later.
        accounts[account_number] = account

        print("\nAccount created successfully!")
        print(account)

    elif choice == "2":
        acc_number = input("Enter account number: ")

        account = accounts.get(acc_number)
        if account is None:
            print("Account not found.")
            continue

        while True:
            print("\n====== ACCOUNT MENU ======")
            print("1. Deposit")
            print("2. Withdraw")
            print("3. Check balance")
            print("4. Show account info")
            print("5. Logout")

            option = input("Choose: ")

            if option == "1":
                account.deposit(read_amount("Amount: "))

            elif option == "2":
                account.withdraw(read_amount("Amount: "))

            elif option == "3":
                account.check_balance()

            elif option == "4":
                print(account)

            elif option == "5":
                print("Logged out.")
                break

            else:
                print("Invalid option.")

    elif choice == "3":
        print("Goodbye!")
        break

    else:
        print("Invalid choice.")
