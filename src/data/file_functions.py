from typing import Union


def load_guesses(file_path: str, with_frequency: bool = False) -> Union[set[str], dict[str, int]]:
    if with_frequency:
        guesses = {}
        with open(file_path, 'r') as f:
            for line in f:
                word, freq = line.strip().split(" ")
                guesses[word.upper()] = int(freq.upper())
        return guesses

    guesses = set()
    with open(file_path, 'r') as f:
        for line in f:
            guesses.add(line.strip().split(" ")[0].upper())

    return guesses


def load_answers(file_path: str) -> set[str]:
    answers = set()
    with open(file_path, 'r') as f:
        for line in f:
            answers.add(line.strip().upper())
    return answers
