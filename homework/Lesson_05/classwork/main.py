try:
    age = int(input("შეიყვანეთ ასაკი: "))

    if age < 0:
        raise TypeError("უარყოფითი ასაკი არ შეიძლება!")

except TypeError as e:
    print(e)

except ValueError:
    print("შეიყვანეთ მხოლოდ რიცხვი!")

else:
    if age < 18:
        print("არასრულწლოვანი")
    else:
        print("სრულწლოვანი")
        
finally:
    print("პროცესი დასრულდა.")