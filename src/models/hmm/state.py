class State:
    def __init__(self, word: str, prob: float = 0.0):
        self.word = word
        self.prob = prob

    def __str__(self):
        return self.word

    def __repr__(self):
        return self.word

    def __eq__(self, other):
        return self.word == other.word

    def __hash__(self):
        return hash(self.word)
