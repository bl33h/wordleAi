import random


def load_answers() -> set:
    """
    Loads the answers from the file
    :return: Set of words
    """
    with open('data/answers.txt', 'r') as f:
        return set(f.read().splitlines())


def load_guesses() -> dict:
    """
    Loads the guesses from the file
    {word: probability}
    :return: Set of guesses
    """
    guesses = {}
    with open('data/guesses.txt', 'r') as f:
        lines = f.read().splitlines()
        for line in lines:
            word, guess = line.split(' ')
            guesses[word] = guess
    return guesses


def parse_letters(word: str) -> dict:
    """
    Parses the letters in the word
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


def pick_answer() -> dict:
    """
    Picks a random answer from the list of answers.
    :return:
    """
    word = random.choice(list(load_answers()))
    answer = {
        "answer": word,
        "length": len(word),
        "letters": parse_letters(word)
    }
    return answer


class Wordle:
    """
    A CLI version of the game Wordle.
    """

    def __init__(self, max_guesses: int = 6):
        self.max_guesses = max_guesses
        self.valid_guesses: dict = load_guesses()
        self.answer: dict = {}
        self.user_guesses: list[tuple] = []

    def reset(self) -> None:
        """
        Resets the game
        :return: None
        """
        self.answer = {}
        self.user_guesses = []

    def guess_word(self, guess: str) -> tuple:
        """
        Returns an encoded version of the guess.
        The way it encodes is as follows:
        - If the letter is not in the word, it is encoded as 0
        - If the letter is in the word but not in the correct position, it is encoded as 1
        - If the letter is in the word and in the correct position, it is encoded as 2
        :param guess: The user's guessed word
        :return: Tuple (<word_guessed, <code>)
        """
        pass

    def play(self) -> None:
        """
        Start Playing
        :return: None
        """
        print("Welcome to Wordle!")
        self.answer = pick_answer()
        print(self.answer)
