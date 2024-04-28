from src.game.wordle import Wordle


def main():
    wordle = Wordle(
        answers_path='data/answers.txt',
        guesses_path='data/guesses.txt',
        max_guesses=6,
        display_answer=True
    )
    wordle.play()


if __name__ == "__main__":
    main()
