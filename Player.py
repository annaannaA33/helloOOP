class Player:
    def __init__(self, name=None):
        self.name = name


def welcome_player(player):
    if player.name:
        print(f"Welcome back, {player.name}!")
    else:
        player.name = input("Enter your name: ")
        print(f"Hello, {player.name}!")
