class bank:

    bank_name = "ABC bank"
    __total_accounts = 0

    def __init__(self, owner: str, balance: int):
        
        self._owner = owner

        bank.__total_accounts += 1
        self.__balance = balance

        self.__account_number = f"AN{bank.__total_accounts:04}"

        if not self.validate_amount(balance):
            print("invalid amount")


    def deposit(self, amount: int):
        
        if self.validate_amount(amount):
            self.__balance += amount
            print(f"{amount} has been added to your balance")
        else:
            print("deposit did not go through")

    def withdraw(self, amount: int):
        if self.validate_amount(amount) and self.__balance - amount >= 0:
            self.__balance -= amount
            print(f"{amount} withdrawn successfuly")
        else:
            print("withdrawal did not go through")

    def check_balance(self):
        print(f"your balance is {self.__balance}")

    
    def get_account_number(self):
        print(f"\nyour account number is {self.__account_number}")
        return self.__account_number

    def change_owner(self, new_owner: str):
        self._owner = new_owner

    @classmethod
    def get_total_accounts(cls):
        return f"total number of accounts are {cls.__total_accounts}"
    
    @staticmethod
    def validate_amount(amount: int):
        return (True if amount > 0 else False)
        
    def __str__(self):
        return f"Account: {self.__account_number} | Owner: {self._owner}"