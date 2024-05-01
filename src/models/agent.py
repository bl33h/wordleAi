from abc import abstractmethod


class Agent:
    def __init__(self):
        self.guesses = []

    @abstractmethod
    def guess(self) -> str:
        pass
