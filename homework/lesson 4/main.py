choice = input("აირჩიეთ ამოცანა (1, 2 ან 3): ")

if choice == "1":

    weight = float(input("შეიყვანეთ წონა (კგ): "))
    height = float(input("შეიყვანეთ სიმაღლე (მ): "))

    bmi = weight / (height ** 2)

    print("BMI =", bmi)

    if bmi < 19:
        print("Underweight")

    elif bmi <= 25:
        print("Normalweight")

    else:
        print("Overweight")


elif choice == "2":

    num1 = float(input("შეიყვანეთ პირველი რიცხვი: "))
    num2 = float(input("შეიყვანეთ მეორე რიცხვი: "))

    operator = input("შეიყვანეთ ოპერატორი (+, -, *, /): ")

    if operator == "+":
        print("შედეგი =", num1 + num2)

    elif operator == "-":
        print("შედეგი =", num1 - num2)

    elif operator == "*":
        print("შედეგი =", num1 * num2)

    elif operator == "/":
        if num2 != 0:
            print("შედეგი =", num1 / num2)
        else:
            print("0-ზე გაყოფა არ შეიძლება!")

    else:
        print("არასწორი ოპერატორი!")


elif choice == "3":

    num1 = int(input("შეიყვანეთ პირველი რიცხვი: "))
    num2 = int(input("შეიყვანეთ მეორე რიცხვი: "))
    num3 = int(input("შეიყვანეთ მესამე რიცხვი: "))

    if num1 == num2 or num1 == num3 or num2 == num3:
        print("გთხოვთ შეიყვანოთ განსხვავებული რიცხვები!")

    else:

        if num1 > num2 and num1 > num3:
            print("ყველაზე დიდი რიცხვია:", num1)

        elif num2 > num1 and num2 > num3:
            print("ყველაზე დიდი რიცხვია:", num2)

        else:
            print("ყველაზე დიდი რიცხვია:", num3)

else:
    print("გთხოვთ აირჩიოთ მხოლოდ 1, 2 ან 3!")