class Bank:

    bank_name = "ABC bank"
    __total_accounts = 0

    def __init__(self, owner: str, balance: int = 0):
        self._owner = owner

        if balance < 0:
            print("Invalid starting balance, defaulting to 0.")
            balance = 0

        self.__balance = balance

        Bank.__total_accounts += 1
        self.__account_number = f"AN{Bank.__total_accounts:04}"

    def deposit(self, amount: int):
        if not self.validate_amount(amount):
            print("Deposit did not go through: amount must be positive.")
            return

        self.__balance += amount
        print(f"{amount} has been added to your balance")

    def withdraw(self, amount: int):
        if not self.validate_amount(amount):
            print("Withdrawal did not go through: amount must be positive.")
            return

        if amount > self.__balance:
            print("Withdrawal did not go through: insufficient funds.")
            return

        self.__balance -= amount
        print(f"{amount} withdrawn successfully")

    def check_balance(self):
        print(f"your balance is {self.__balance}")

    def get_balance(self):
        return self.__balance

    def get_account_number(self):
        return self.__account_number

    def change_owner(self, new_owner: str):
        self._owner = new_owner

    @classmethod
    def get_total_accounts(cls):
        return f"total number of accounts are {cls.__total_accounts}"

    @staticmethod
    def validate_amount(amount: int):
        return amount > 0

    def __str__(self):
        return f"Account: {self.__account_number} | Owner: {self._owner}"
