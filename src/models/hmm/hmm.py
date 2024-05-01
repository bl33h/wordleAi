from src.data.file_functions import load_guesses
from src.models.agent import Agent
from src.models.hmm.state import State


def create_states() -> list[State]:
    guesses: set[str] = load_guesses('data/guesses.txt', with_frequency=False)
    states = []
    individual_prob = 1 / len(guesses)
    for guess in guesses:
        states.append(State(guess, individual_prob))
    return states


class HMM(Agent):
    """
    A Hidden Markov Model for the game Wordle.
    """

    def __init__(self):
        super().__init__()
        self.states = create_states()

    def guess(self) -> str:
        """
        Guesses the word.
        :return: The guess
        """
        return "CRANE"
