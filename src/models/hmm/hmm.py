from hmmlearn import hmm

from src.data.file_functions import *
from src.feedback import Feedback as f
from src.models.agent import Agent


class HMM(Agent):
    """
    A Hidden Markov Model (HMM) agent for the Wordle game.
    """
    def __init__(self):
        super().__init__()

    def guess(self) -> str:
        """
        The agent tries to guess the word based on the model.
        :return: The agent's guess
        """
        pass
