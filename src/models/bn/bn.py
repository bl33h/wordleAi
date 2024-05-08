from models.agent import Agent
from data.file_functions import load_guesses
from random import choice

class BN(Agent):

    def __init__(self):
        super().__init__()
        def define_posible_words(self):
            for word in self.guess_words:
                self.posible_words[word] = 1/len(self.guess_words)
        self.guess_words = load_guesses('src/data/guesses.txt')
        self.posible_words = {}
        define_posible_words(self)
        self.letters = {}

    def update_probs(self):

        def get_letters(self):
            wletters = {}
            lletters = {}
            for letter in self.letters:
                if self.letters[letter][0] == 1 or self.letters[letter][0] == 2:
                    wletters[letter] = self.letters[letter]
                else:
                    lletters[letter] = self.letters[letter]
            return wletters, lletters
        
        def higher_exist(wletters):
            for letter in wletters:
                if wletters[letter][0] == 2:
                    return True
            return False

        def letters_in_word(wletters, lletters, word, flag):
            
            for letter in lletters:
                if letter in word:
                    return False
            
            if flag:
                for letter in wletters:
                    if letter not in word:
                        return False
                    elif wletters[letter][0] == 2 and word[wletters[letter][1]] != letter:
                        return False
                    elif wletters[letter][0] == 1 and word[wletters[letter][1]] == letter:
                        return False
                return True
            else:
                for letter in wletters:
                    if letter not in word:
                        return False
                    elif wletters[letter][0] == 1 and word[wletters[letter][1]] == letter:
                            return False
                return True
            


        def is_higher_word(wletters, word):
            counter = 0
            for letter in wletters:
                if wletters[letter][0] == 2 and word[wletters[letter][1]] == letter:
                    counter += 1
            return counter
                    

        higher_words = {}
        wletters, lletters = get_letters(self)
        flag = higher_exist(wletters)
        for word in self.posible_words:
            if self.posible_words[word] != 0:
                if letters_in_word(wletters, lletters, word, flag):
                    if flag:
                        higher = is_higher_word(wletters, word)
                        higher_words[word] = higher
                    else:
                        higher_words[word] = 1
                else:
                    self.posible_words[word] = 0

                
        higher_count = sum(list(higher_words.values()))

        for word in self.posible_words:
            if word in higher_words:
                self.posible_words[word] = 1/higher_count*higher_words[word]
            else:
                self.posible_words[word] = 0
            


        

    def guess(self) -> str:
        if self.guesses:
            ac_guess = None
            for i in range(len(self.guesses)):
                if self.guesses[5-i] is not None:
                    ac_guess = self.guesses[5-i]
                    break
            guess_word = ac_guess[0]
            code = ac_guess[1]
            for i, letter in enumerate(guess_word):
                if code[i] == '2':
                    self.letters[letter] = (2,i)
                elif code[i] == '1':
                    if letter in self.letters:
                        if self.letters[letter] != '2':
                            self.letters[letter] = (1,i)
                    else:
                        self.letters[letter] = (1,i)
                else:
                    if letter in self.letters:
                        if self.letters[letter] != 2 and self.letters[letter] != 1:
                            continue
                    else:
                        self.letters[letter] = (0,i)
            
            self.update_probs()

            prob_words = []
            max_prob = max(list(self.posible_words.values()))

            for word in self.posible_words:
                if self.posible_words[word] >= max_prob:
                    prob_words.append(word)

            return choice(prob_words)
        else:
            return choice(["TRACE", "SALET", "CREATE"])