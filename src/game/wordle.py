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
        "letters": parse_letters(word)
    }
    return answer


class Wordle:
    """
    A CLI version of the game Wordle.
    """

    def __init__(self, max_guesses: int = 3):
        self.max_guesses = max_guesses
        self.valid_guesses: dict = load_guesses()

        self.answer = {}
        self.user_guesses = []

    def reset(self) -> None:
        """
        Resets the game
        :return: None
        """
        self.answer = {}
        self.user_guesses = []

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
                    code += "2"
                else:
                    code += "1"
                answer_letters[letter] -= 1
            else:
                code += "0"

        return guess, code

    def get_row_display(self, encoded_guess: str = None) -> str:
        """
        Get the row for the guess
        :param encoded_guess: The user's guess
        :return: The row
        """
        if not encoded_guess:
            return "▢▢▢▢▢"
        else:
            # Encode with answers
            return "AAAAA"

    def get_guess(self) -> str:
        """
        Get the user's guess by showing the current state of the game
        :return: The user's guess
        """
        # for i in range(self.max_guesses):
        #     print(self.get_row_display(self.user_guesses[i]))

        user_guess = input("Enter your guess: ")
        return user_guess

    def play(self) -> None:
        """
        Start Playing
        :return: None
        """
        # self.answer = pick_answer()
        self.answer = {"answer": "helos", "letters": parse_letters("helos")}
        self.user_guesses: list[tuple[str, str]] | list[None] = [None] * self.max_guesses
        has_won = False

        print(self.answer)

        # Main game loop
        for i in range(self.max_guesses):
            if has_won:
                break

            user_guess = self.get_guess()
            self.user_guesses[i] = self.encode_guess(user_guess)

            print(self.user_guesses)

            has_won = user_guess == self.answer['answer']

        # End of game
        if has_won:
            print("You have won!")
        else:
            print("You have lost!")
