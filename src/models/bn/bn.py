from src.models.agent import Agent
from src.data.file_functions import load_guesses

class BN(Agent):

    def __init__(self):
        super().__init__()
        self.posible_words = load_guesses("data/guesses.txt")
        for word in self.posible_words:
            self.posible_words[word] = 1/len(self.posible_words)
        self.letters = {}

    def update_probs(self):
        count = 0
        higher_words = []
        words = []
        for word in self.posible_words:
            for letter in self.letters:
                if self.letters[letter] == None:
                    continue
                elif (self.letters[letter][0] == 1 or self.letters[letter][0] == 2) and letter in word:
                    count += 1
                    if self.letters[letter][0] == 2 and word[self.letters[letter][1]] == letter:
                        higher_words.append(word)
                        words.append(word)
                    elif self.letters[letter][0] == 1:
                        words.append(word)
                else:
                    self.posible_words[word] = 0 
        higher_count = len(higher_words)

        for word in words:
            self.posible_words[word] = 0.6/len(words)
            if word in higher_words:
                self.posible_words[word] += 0.4/higher_count


                    


    def guess(self) -> str:
        word = self.guesses[-1][0]
        code = self.guesses[-1][1]
        for i, letter in enumerate(word):
            if code[i] == 2 and (self.letters[letter] == 1 or self.letters[letter] == None):
                self.letters[letter] = (2,i)
            elif code[i] == 1 and (self.letters[letter] == 0 or self.letters[letter] == None):
                self.letters[letter] = (1,i)

        pass