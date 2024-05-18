from game.wordle import Wordle
from models.constraints.constraints import Constraints
from models.user.user import User
from models.minimax.minimax import Minimax


def main():
    wordle = Wordle(
        answers_path='src/data/answers.txt',
        guesses_path='src/data/guesses.txt',
        max_guesses=6,
        display_answer=True
    )
    # wordle.set_agent(Constraints())
    wordle.set_agent(Minimax())
    # wordle.set_agent(User())
    wordle.play()


if __name__ == "__main__":
    main()
