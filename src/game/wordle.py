import random
import time
from models.agent import Agent
from feedback import Feedback as f
from data.file_functions import load_answers, load_guesses

def parse_letters(word: str) -> dict:
    """
    Parses the letters in the word into a dictionary that tracks the count of each letter.
    """
    letters = {}
    for letter in word:
        letters[letter] = letters.get(letter, 0) + 1
    return letters


def pick_answer(file_path: str) -> dict:
    """
    Picks a random answer from the list of answers loaded from the given file path.
    """
    word = random.choice(list(load_answers(file_path)))
    return {"answer": word, "letters": parse_letters(word)}


def display_row(guess: tuple[str, str] = None) -> None:
    """
    Displays a row for the given guess with colors corresponding to the guess accuracy.
    """
    if not guess:
        print("▢▢▢▢▢")
    else:
        word, code = guess
        for i, letter in enumerate(word):
            color = '\033[90m' if code[i] == f.GRAY.value else '\033[92m' if code[i] == f.GREEN.value else '\033[93m'
            print(f"{color}{letter}\033[0m", end="")
        print()


def encode_guess(answer_param: dict, guess: str) -> tuple[str, str]:
    """
    Encodes the user's guess based on the current answer, marking letters as correct, misplaced, or incorrect.
    """
    answer, answer_letters = answer_param['answer'], answer_param['letters'].copy()
    code = ""
    for i, letter in enumerate(guess):
        if letter in answer_letters and answer_letters[letter] > 0:
            code += f.GREEN.value if answer[i] == letter else f.YELLOW.value
            answer_letters[letter] -= 1
        else:
            code += f.GRAY.value
    return guess, code


class Wordle:
    """
    A command-line version of the Wordle game.
    """

    def __init__(self, answers_path: str, guesses_path: str, max_guesses: int = 6, display_answer: bool = False):
        self.display_answer = display_answer
        self.answers_path, self.guesses_path = answers_path, guesses_path
        self.max_guesses = max_guesses
        self.valid_guesses = load_guesses(guesses_path)
        self.reset()

    def reset(self):
        """
        Resets the game state to start a new game.
        """
        self.answer = pick_answer(self.answers_path)
        self.user_guesses = [None] * self.max_guesses
        self.has_won = self.is_game_finished = False

    def set_answer(self, word: str):
        """
        Sets a specific word as the answer for testing purposes.
        """
        self.answer = {'answer': word, 'letters': parse_letters(word)}
        self.reset()

    def set_agent(self, agent: Agent):
        """
        Sets the agent responsible for making guesses.
        """
        self.agent = agent
        self.agent.guesses = self.user_guesses

    def get_guess(self) -> str:
        """
        Retrieves a valid guess from the agent.
        """
        self.display_guesses()
        while True:
            agent_guess = self.agent.guess()
            if agent_guess in self.valid_guesses:
                return agent_guess
            time.sleep(1)  # Slight delay to mimic thinking time

    def play(self):
        """
        Executes the game loop until the game is finished.
        """
        for i in range(self.max_guesses):
            user_guess = self.get_guess()
            self.user_guesses[i] = encode_guess(self.answer, user_guess)
            self.agent.guesses = self.user_guesses
            self.has_won = user_guess == self.answer['answer']
            if self.has_won:
                break
        self.is_game_finished = True
        self.display_guesses()
        print("You have won!" if self.has_won else f"You have lost! The word was {self.answer['answer']}")

    def display_guesses(self):
        """
        Displays all the guesses made so far in the game.
        """
        print("====================================")
        for guess in self.user_guesses:
            display_row(guess)
        print("====================================")

    def get_possible_guesses(self) -> list[str]:
        """
        Get the possible guesses
        :return: List of possible guesses
        """
        return list(self.valid_guesses)

    def get_possible_answers(self) -> list[str]:
        """
        Get the possible answers
        :return: List of possible answers
        """
        return list(load_answers(self.answers_path))

    def get_state(self) -> dict:
        """
        Get the current state of the game
        :return: The state of the game
        """
        return {"answer_word": self.answer['answer'], "answer_letters": self.answer['letters'],
                "is_game_finished": self.is_game_finished, "has_won": self.has_won, "user_guesses": self.user_guesses,
                "guesses_made": len([guess for guess in self.user_guesses if guess]), "max_guesses": self.max_guesses, }
