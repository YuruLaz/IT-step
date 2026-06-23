import random
choice = int(input("ამოირჩიეთ ამოცანა (1, 2, 3, 4):"))
if choice == 1:
    #ეს ცვლადი იმისათვის რომ დავნიშნოთ რამდენი მთელი რიცხვი გვექნება ლისტში
    random_number_count = random.randint(5, 15)

    #list comperhantion მაგდენი რიცხვის დასაგენერირებლად
    my_list = [random.randint(1, 100) for _ in range(random_number_count)]

    #არ ვიყენებ sum() და len() ფუნქციებს
    sum_list = 0
    list_count = 0

    for i in my_list:
        list_count += 1
        sum_list += i

    average_list = sum_list/list_count

    print(my_list)
    print(f"ამ ლისტში {list_count} ინტეჯერია\nამ ლისტის ჯამი - {sum_list}, ხოლო მისი საშუალო - {average_list:.2f}")

elif choice == 2:
    just_list = ['a', 'b', 2, 4, 2, 'c', 'j', 1, 'b', 'd', 'c', 4, 1]
    popped_values = []

    #just_list-ის იტერაცია უკნიდან range(ბოლო ინდექსი, გაჩერდი -1მდე, ბიჯი -1)
    for i in range(len(just_list)-1, -1, -1):
        #ვიჭერთ just_list[i]
        #slice [:i] ყველაფერი დასაწყისიდან just_list[i]-მდე
        if just_list[i] in just_list[:i]:
            popped_values.append(just_list.pop(i))

    print(just_list)
    print(f"popped values - {popped_values}")

elif choice == 3:
    #pretty straight-forward
    new_list = [random.randint(-50, 50) for _ in range(0, 20)]
    even_num_list = []
    for i in new_list:
        if i%2 == 0:
            even_num_list.append(new_list.pop(new_list.index(i)))
    print(new_list)
    print(even_num_list)

elif choice == 4:
    persons = [
    ('Kelly', 'Simpson', 26),
    ('Erika', 'Stephens', 24),
    ('Cheryl', 'Dunn', 30),
    ('Amy', 'Larsen', 49),
    ('Christine', 'Gordon', 23),
    ('Monica', 'Huff', 38),
    ('David', 'Nixon', 36),
    ('Cindy', 'Escobar', 41),
    ('Cindy', 'White', 33), 
    ('Joel', 'Hall', 43),
    ('Steven', 'Winters', 28),
    ('Alex', 'Cole', 68),
    ('Alex', 'Smith', 32),
    ('Alex', 'White', 42),
    ('Brittany', 'Thompson', 18),
    ('Ernest', 'Young', 43),
    ('Traci', 'Wells', 38),
    ('Andrew', 'Flores', 61),
    ('Christopher', 'Lewis', 29),
    ('Kevin', 'Willis', 57),
    ('Kayla', 'Lucas', 28),
    ('Michelle', 'Rush', 43),
    ('Thomas', 'Mason', 37)
]   
    
    while True:
        person_guess = input("\nშეიყვანე სახელი (ან 'stop'): ").lower()

        if person_guess == "stop":
            break

        new_person_list = []

        for person in persons:
            if person[0].lower() == person_guess:
                new_person_list.append(person)

        if not new_person_list:
            print("ასეთი სახელი არ მოიძებნა")
            continue

        print(new_person_list)

        surname_guess = input("\nშეიყვანე გვარი (ან 'stop'): ").lower()

        if surname_guess == "stop":
            break

        for person in new_person_list:
            if person[1].lower() == surname_guess:
                print(f"ადამიანის ასაკი არის: {person[2]}")
                break
        else:
            print("ასეთი გვარი არ მოიძებნა")


