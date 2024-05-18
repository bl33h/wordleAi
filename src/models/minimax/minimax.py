import itertools

import numpy as np

from src.data.file_functions import *
from src.feedback import Feedback as f
from src.game.wordle import parse_letters, encode_guess
from src.models.agent import Agent


def get_feedback(guess: str, supposed_answer: str) -> tuple[str]:
    answer = {'answer': supposed_answer, 'letters': parse_letters(supposed_answer)}
    encoded_guess = encode_guess(answer, guess)
    return tuple(encoded_guess[1])


def get_outcomes(guess: str, remaining_words: list[str]) -> dict:
    outcomes = {}
    elements = [f.GREEN.value, f.YELLOW.value, f.GRAY.value]
    for combination in itertools.product(elements, repeat=5):
        outcomes[combination] = []

    for word in remaining_words:
        feedback = get_feedback(guess, word)
        if feedback in outcomes:
            outcomes[feedback].append(word)
        else:
            outcomes[feedback] = [word]
    return outcomes


def minimax(candidate_words: list[str], remaining_words: list[str]):
    best_score = float('inf')
    best_guess = None
    best_outcomes = None

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
        self.words = list(load_guesses('data/guesses.txt'))
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
