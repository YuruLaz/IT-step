try:
    age = int(input("შეიყვანეთ ასაკი: "))

    if age < 0:
        raise ValueError("უარყოფითი ასაკი არ შეიძლება!")

except ValueError:
    print("შეიყვანეთ მხოლოდ რიცხვი!")

else:
    if age < 18:
        print("არასრულწლოვანი")
    else:
        print("სრულწლოვანი")