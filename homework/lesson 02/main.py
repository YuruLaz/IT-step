import math

while True:
    choice = input("აირჩიეთ ამოცანა (1 ან 2): ")

    #ამოცანა 1: ჰიპოთენუზა და სამკუთხედის გამოთვლა
    if choice == "1":
        
        while True:
        #while loop-ი დადებითი რიცხვის ვალიდაციისთვის

            a = input("\nშეიყვანეთ პირველი კათეტი (სმ): ")

            if a.isdigit() and int(a) > 0:
            #შემოწმება - თუ დადებითი, break
                a = int(a)
                break
            print("შეიყვანეთ დადებითი მთელი რიცხვი!")


        while True:
        #იგივე ოპერაცია რაც ზემოთ, მეორა კათეტისთვის

            b = input("შეიყვანეთ მეორე კათეტი (სმ): ")

            if b.isdigit() and int(b) > 0:
                b = int(b)
                break
            print("შეიყვანეთ დადებითი მთელი რიცხვი!")

        hypotenuse = math.sqrt(a**2 + b**2)
        area = (a * b) / 2
        #გამოთვლა

        print(f"\nჰიპოთენუზა = {hypotenuse} სმ")
        print(f"ფართობი = {area} სმ²")

        break
        #დასრულება ამოცანა 1-ის და break loop-იდან

    #ამოცანა 2: წამების კონვერტაცია
    elif choice == "2":
        
        while True:
        #while loop-ი დადებითი რიცხვის ვალიდაციისთვის

            seconds = input("\nშეიყვანეთ წამების რაოდენობა: ")

            if seconds.isdigit():
            #შემოწმება - თუ დადებითი, break
                seconds = int(seconds)
                break

            print("შეიყვანეთ მხოლოდ მთელი რიცხვი!")

        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        remaining_seconds = seconds % 60
        #გამოთვლა

        print(f"\n{seconds} წამი უდრის - {hours} საათს, {minutes} წუთს და {remaining_seconds} წამს.")

        break
        #დასრულება ამოცანა 2-ის და break loop-იდან

    else:
        #ვალიდაცია მხოლოდ 1 ან 2-ის არჩევისთვის
        print("გთხოვთ აირჩიოთ მხოლოდ 1 ან 2!")