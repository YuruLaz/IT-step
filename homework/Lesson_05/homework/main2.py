try:
    num1 = float(input("შეიყვანეთ პირველი რიცხვი: "))
    num2 = float(input("შეიყვანეთ მეორე რიცხვი: "))

    result = num1 / num2

except ValueError:
    print("შეიყვანეთ მხოლოდ რიცხვები!")

except ZeroDivisionError:
    print("ნულზე გაყოფა არ შეიძლება!")

except Exception as e:
    print("დაფიქსირდა უცნობი შეცდომა:", e)

else:
    print("შედეგი =", result)

finally:
    print("პროგრამა დასრულდა")