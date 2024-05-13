from game.wordle import Wordle
from models.bn.bn import BN
from models.user.user import User


def main():
    wordle = Wordle(
        answers_path='src/data/answers.txt',
        guesses_path='src/data/guesses.txt',
        max_guesses=6,
        display_answer=True
    )
    wordle.set_agent(BN())
    # wordle.set_agent(HMM())
    wordle.play()


if __name__ == "__main__":
    main()
