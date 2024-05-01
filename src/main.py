from src.game.wordle import Wordle
from src.models.hmm.hmm import HMM
from src.models.user.user import User


def main():
    wordle = Wordle(
        answers_path='data/answers.txt',
        guesses_path='data/guesses.txt',
        max_guesses=6,
        display_answer=True
    )
    wordle.set_agent(HMM())
    wordle.play()


if __name__ == "__main__":
    main()
