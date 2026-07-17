import json


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"Person: ({self.name}, {self.age})"



# 1
def serialize(person):
    return f"Name: {person.name}, Age: {person.age}"


def deserialize(text):
    parts = text.split(", ")

    name = parts[0].split(": ")[1]
    age = int(parts[1].split(": ")[1])

    return Person(name, age)



p1 = Person("Otar", 35)


with open("person.txt", "w") as file:
    file.write(serialize(p1))


with open("person.txt", "r") as file:
    data = file.read()


new_person = deserialize(data)

print("Deserialized object:")
print(new_person)



# 2
def add_persons(count):
    try:
        with open("persons.json", "r") as file:
            persons = json.load(file)

    except FileNotFoundError:

        persons = []


    if persons:
        last_id = persons[-1]["id"]
    else:
        last_id = 0


    for _ in range(count):
        name = input("Enter your name: ")
        age = int(input("Enter your age: "))

        last_id += 1

        new_person = {
            "id": last_id,
            "name": name,
            "age": age
        }

        persons.append(new_person)


    with open("persons.json", "w") as file:
        json.dump(persons, file, indent=4)

    print("\nUpdated persons.json successfully!")


add_persons(2)