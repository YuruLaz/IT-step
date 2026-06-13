choice = input("აირჩიეთ ამოცანა (1, 2 ან 3): ")

if choice == "1":
    #ვალიდაცია იმისათვის რომ შემოყვანილი რიცხვი იყოს ნამდვილი და დადებითი
    while True:
        try:
            number_for_fac = int(input("შეიყვანეთ რიცხვი: "))

            if number_for_fac >= 0:
                break

            print("გთხოვთ შეიყვანოთ დადებითი რიცხვი.")

        except ValueError:
            print("გთხოვთ შეიყვანოთ სწორი რიცხვი.")
    #---------------------------------

    factorial = 1

    for i in range(2, number_for_fac + 1):
        factorial *= i

    #ან ჩაშენებული ფუნქციის გამოყენებით
    import math

    factorial = math.factorial(number_for_fac)
    #----------------------

    print(f"{number_for_fac}-ის ფაქტორიალი არის: {factorial}")

elif choice == "2":
    print("გამრავლების ტაბულა for ციკლებით")

    for i in range(1, 11):
        print(f"\n{i}-ის გამრავლების ცხრილი")

        for j in range(1, 11):
            print(f"{i} * {j} = {i*j}")

elif choice == "3":
    to_be_paid = 50

    print(f"\nგადასახდელია {to_be_paid}")

    while to_be_paid > 0:
        try:
            inserted_money = int(input("შეიყავენთ კუპიურა (5, 10, 20):"))

            if inserted_money not in (5, 10, 20):
                print("გთხოვთ შეიყვანოთ მხოლოდ 5, 10 ან 20\n")
                continue    

            to_be_paid -= inserted_money
            
            if to_be_paid == 0:
                print("თქვენ სრულიად ამოწურეთ გადასახადი, გმადლობთ!")
                break
            elif to_be_paid < 0:
                print(f"გადასახდელი გადახდილია! თქვენი ხურდა: {to_be_paid*-1} ლარი")
            else:
                print(f"დარჩა გადასახადი {to_be_paid}\n")

        except ValueError:
            print("შეიყვანეთ მხოლოდ რიცხვი!\n")

