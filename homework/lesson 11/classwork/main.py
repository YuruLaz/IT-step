from faker import Faker
import random

fake = Faker()

def generate_student(id: int) -> dict:
    return {
        "ID": id,
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "age": random.randint(18, 80)
    }

def generate_students(count: int) -> list:
    return [generate_student(i + 1) for i in range(count)]

print(generate_students(3))