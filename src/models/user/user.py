from models.agent import Agent


class User(Agent):
    def __init__(self):
        super().__init__()

    def guess(self) -> str:
        """
        Get the user's guess by showing the current state of the game
        :return: The user's guess
        """
        return input("Enter your guess: ").upper()
