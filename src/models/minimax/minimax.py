import itertools

import numpy as np

from data.file_functions import *
from feedback import Feedback as f
from game.wordle import parse_letters, encode_guess
from models.agent import Agent


def get_feedback(guess: str, supposed_answer: str) -> tuple[str]:
    """
    Get the feedback of a guess by comparing it to another word, encoding it like the game would.
    :param guess: the currently evaluated guess
    :param supposed_answer: the word that acts as the answer
    :return: the feedback of the guess as a tuple (for it to be used by itertools keys)
    """
    answer = {'answer': supposed_answer, 'letters': parse_letters(supposed_answer)}
    encoded_guess = encode_guess(answer, guess)  # Uses the same encoding function as the game
    return tuple(encoded_guess[1])


def get_outcomes(guess: str, remaining_words: list[str]) -> dict[tuple[str], list[str]]:
    """
    Get the outcomes of a guess by comparing it to a list of words.
    Each key is a one of the 5^3 possible feedbacks and the value is a list of words that have that feedback when compared
    to the guess.
    :param guess: The guess to be compared to the words
    :param remaining_words: The list of words to be compared to the guess
    :return: A dictionary with the feedbacks as keys and the words that have that feedback as values
    """
    outcomes = {}
    elements = [f.GREEN.value, f.YELLOW.value, f.GRAY.value]
    # Create all the feedbacks possible via permutations with repetition of length 5
    for combination in itertools.product(elements, repeat=5):
        outcomes[combination] = []

    # Get the feedback of each word and add it to the outcomes
    for word in remaining_words:
        feedback = get_feedback(guess, word)
        outcomes[feedback].append(word)

    return outcomes


def minimax(candidate_words: list[str], remaining_words: list[str]):
    """
    Minimax algorithm to find the best guess to make.

    It's designed to minimize the worst-case potential loss or maximize the worst-case potential gain.
    In the context of this game, the algorithm is used to make the guess that minimizes the maximum possible number of
    remaining words.
    :param candidate_words: The list of words to choose from
    :param remaining_words: The list of words that have the same feedback as the guess
    :return: The best guess, the worst-case score (the length of the pool of words), and the outcomes of the guess
    """
    # Initialize the best score with infinity
    best_score = float('inf')  # Stores the length of the pool of words
    best_guess = None  # Stores the best word to guess
    best_outcomes = None  # Stores the outcomes of the best guess

    # Find the word with the maximum number of remaining words
    for guess in candidate_words:
        outcomes = get_outcomes(guess, remaining_words)
        worst_case = max(len(words) for words in outcomes.values())

        if worst_case < best_score:
            best_score = worst_case
            best_guess = guess
            best_outcomes = outcomes

    return best_guess, best_score, best_outcomes


class Minimax(Agent):
    def __init__(self, max_depth: int = 5):
        super().__init__()
        self.max_depth = max_depth
        self.words = list(load_guesses('src/data/guesses.txt'))
        self.outcomes = {}
        self.last_guess_idx = 0

    def guess(self) -> str:
        if not self.guesses:  # First Guess
            choice = np.random.choice(['CRATE', 'TRACE', 'SALET'])
            self.outcomes = get_outcomes(choice, self.words)
            return choice

        # Other guesses
        result = self.guesses[self.last_guess_idx][1]  # The feedback of the last guess
        result = tuple(result)  # Convert to tuple because of the itertools key
        remaining_words = self.outcomes[result]

        if len(remaining_words) == 1:  # If there is only one word left
            return remaining_words[0]
        elif len(remaining_words) == 0:  # If there are no words left
            raise Exception('There are no words with the specified feedback')

        candidate_words = self.words
        best_guess, _, outcomes = minimax(candidate_words, remaining_words)
        self.outcomes = outcomes

        self.last_guess_idx += 1
        return best_guess
