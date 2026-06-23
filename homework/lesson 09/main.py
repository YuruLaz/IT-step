choice = int(input("ამოირჩიეთ ამოცანა (1, 2):"))

if choice == 1:
    def count_uppercase(text):
        count = 0

        for char in text:
            if char.isupper():
                count += 1

        return count, text.upper()


    user_text = input("შეიყვანეთ ტექსტი: ")

    uppercase_count, upper_text = count_uppercase(user_text)

    print(f"დიდი ასოების რაოდენობა: {uppercase_count}")
    print(f"Uppercase ტექსტი: {upper_text}")

elif choice == 2:
    def camel_to_snake(text):
        result = ""

        for char in text:
            if char.isupper():
                result += "_" + char.lower()
            else:
                result += char

        return result


print(camel_to_snake("firstName"))
print(camel_to_snake("name"))
print(camel_to_snake("preferredFirstName"))
print(camel_to_snake("lastName"))