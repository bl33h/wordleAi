import random

from data.file_functions import load_answers, load_guesses
from models.agent import Agent
from feedback import Feedback as f

def parse_letters(word: str) -> dict:
    """
    Parses the letters in the word to a dictionary that keeps track of the amount of each letter in the word.
    :param word: The word to parse
    :return: Dictionary of letters
    """
    letters = {}
    for letter in word:
        if letter in letters:
            letters[letter] += 1
        else:
            letters[letter] = 1
    return letters


def pick_answer(file_path: str) -> dict:
    """
    Picks a random answer from the list of answers.
    :return:
    """
    word = random.choice(list(load_answers(file_path)))
    answer = {"answer": word, "letters": parse_letters(word)}
    return answer


def display_row(guess: tuple[str, str] = None) -> None:
    """
    Get the row for the guess
    :param guess: The user's guess
    :return: The row
    """
    if not guess:
        print("▢▢▢▢▢")
    else:
        # Encode with answers
        word, code = guess
        for i, letter in enumerate(word):
            if code[i] == f.GREEN.value:
                print(f"\033[92m{letter}\033[0m", end="")
            elif code[i] == f.YELLOW.value:
                print(f"\033[93m{letter}\033[0m", end="")
            else:  # GRAY
                print(f"\033[90m{letter}\033[0m", end="")
        print()


class Wordle:
    """
    A CLI version of the game Wordle.
    """

    def __init__(self, answers_path: str, guesses_path: str, max_guesses: int = 6, display_answer: bool = False):
        self.display_answer = display_answer
        self.answers_path = answers_path
        self.guesses_path = guesses_path

        self.max_guesses = max_guesses
        self.valid_guesses: dict = load_guesses(guesses_path)

        self.answer = {}
        self.user_guesses = []

        self.has_won = False
        self.is_game_finished = False
        self.used_letters = []
        self.agent = None

    def reset(self) -> None:
        """
        Resets the game
        :return: None
        """
        self.answer = {}
        self.user_guesses = []
        self.has_won = False
        self.is_game_finished = False
        self.used_letters = []

    def set_agent(self, agent: Agent) -> None:
        """
        Set the agent for the game
        :param agent: The agent to set
        :return: None
        """
        self.agent = agent
        self.agent.guesses = self.user_guesses

    def encode_guess(self, guess: str) -> tuple[str, str]:
        """
        Returns an encoded version of the guess.
        The way it encodes is as follows:
        - If the letter is not in the word, it is encoded as 0
        - If the letter is in the word but not in the correct position, it is encoded as 1
        - If the letter is in the word and in the correct position, it is encoded as 2
        :param guess: The user's guessed word
        :return: Tuple (<word_guessed, <code>)
        """
        answer = self.answer['answer']
        answer_letters = self.answer['letters'].copy()
        code = ""

        for i, letter in enumerate(guess):
            if letter in answer_letters and answer_letters[letter] > 0:
                if answer[i] == letter:
                    code += f.GREEN.value
                else:
                    code += f.YELLOW.value
                answer_letters[letter] -= 1
            else:
                code += f.GRAY.value

        return guess, code

    def get_guess(self) -> str:
        """
        Get the user's guess by showing the current state of the game
        :return: The user's guess
        """
        self.display_guesses()
        agent_guess = ""
        valid_guess = False
        while not valid_guess:
            agent_guess = self.agent.guess()
            valid_guess = agent_guess in self.valid_guesses

        return agent_guess

    def display_guesses(self) -> None:
        """
        Display the user's guesses
        :return:
        """
        if self.display_answer:
            print("====================================")
            print(f"Answer: {self.answer['answer']}")
        print("====================================")
        for j in range(self.max_guesses):
            display_row(self.user_guesses[j])
        print("====================================")

    def play(self) -> None:
        """
        Start Playing
        :return: None
        """
        self.reset()

        self.answer = pick_answer(self.answers_path)
        self.user_guesses: list[tuple[str, str]] | list[None] = [None] * self.max_guesses

        # Main game loop
        for i in range(self.max_guesses):
            if self.has_won:
                break

            user_guess = self.get_guess()
            self.user_guesses[i] = self.encode_guess(user_guess)
            self.agent.guesses = self.user_guesses

            self.has_won = user_guess == self.answer['answer']

        # End of game
        self.is_game_finished = True
        self.display_guesses()
        if self.has_won:
            print("You have won!")
        else:
            print(f"You have lost! The word was {self.answer['answer']}")

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
