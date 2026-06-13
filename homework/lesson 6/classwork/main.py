import random

lives = 5
number_to_guess = random.randint(1, 100)
while lives > 0:
    try:
        guess = int(input("შეიყვანეთ რიცხვი 1-დან 100-მდე: "))
        
        if guess < 1 or guess > 100:
            raise ValueError("გთხოვთ შეიყვანოთ რიცხვი 1-დან 100-მდე.")
        
        if guess == number_to_guess:
            print("გილოცავთ! თქვენ მოიგეთ!")
            break
        elif guess < number_to_guess:
            print("თქვენი რიცხვი ნაკლებია. სცადეთ კიდევ ერთხელ.")
        else:
            print("თქვენი რიცხვი მეტია. სცადეთ კიდევ ერთხელ.")

        lives -= 1
        print(f"დარჩენილია {lives} ცდა.")
    
    except ValueError as e:
        print(e)

if lives == 0:
    print(f"თქვენ წააგეთ! სწორი რიცხვი იყო {number_to_guess}.")