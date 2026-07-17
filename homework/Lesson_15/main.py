from football_team import FootballTeam

team_name = input("Enter team name: ")
coach = input("Enter coach name: ")

team = FootballTeam(team_name, coach)

while True:
    print("\nFOOTBALL TEAM OPTIONS")
    print("1. Add Player")
    print("2. Remove Player")
    print("3. Update Player")
    print("4. Show Team Information")
    print("5. Show Player Information")
    print("6. Exit")

    choice = input("Choose (1, 2, 3, 4, 5 or 6 to exit): ")

    if choice == "1":

        name = input("Player name: ")
        position = input("Position: ")
        number = int(input("Number: "))
        age = int(input("Age: "))
        nationality = input("Nationality: ")

        team.add_player(name, position, number, age, nationality)


    elif choice == "2":

        number = int(input("Enter player number: "))
        team.remove_player(number)


    elif choice == "3":

        number = int(input("Enter player number: "))
        key = input("What do you want to update? (goals, assists, age...): ")
        value = input("New value: ")

        if value.isdigit():
            value = int(value)

        team.update_player(number, key, value)

    elif choice == "4":
        team.show_team_info()

    elif choice == "5":
        number = int(input("Enter player number: "))
        team.show_player_info(number)

    elif choice == "6":
        break

    else:
        print("Invalid choice")