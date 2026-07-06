class FootballTeam:
    def __init__(self, team_name, coach):
        self.team_name = team_name
        self.coach = coach
        self.players = []

    def add_player(self, name, position, number, age, nationality):

        player = {
            "name": name,
            "position": position,
            "number": number,
            "age": age,
            "nationality": nationality
        }
        self.players.append(player)
        print("Player added")


    def remove_player(self, number):

        for player in self.players:
            if player["number"] == number:
                self.players.remove(player)
                print("Player removed")
                return
        print("Player not found")


    def update_player(self, number, key, value):

        for player in self.players:
            if player["number"] == number:
                player[key] = value
                print("Player updated")
                return
        print("Player not found")


    def show_team_info(self):

        print("\nTEAM INFO")

        print("Team:", self.team_name)
        print("Coach:", self.coach)
        print("\nPlayers:")
        if not self.players:
            print("No players.")
        else:
            for player in self.players:
                print(player)


    def show_player_info(self, number):

        for player in self.players:
            if player["number"] == number:
                print(player)
                return
        print("Player not found!")