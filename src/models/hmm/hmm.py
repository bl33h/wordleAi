from hmmlearn import hmm
from models.agent import Agent
from data.file_functions import load_guesses
from random import choice
import numpy as np


class HMM(Agent):
    """
    A Hidden Markov Model (HMM) agent for the Wordle game.
    """
    def __init__(self):
        super().__init__()
        self.guess_words = load_guesses('src/data/guesses.txt')
        self.states = list(self.guess_words)
        self.n_states = len(self.states)

        # Inicializar las matrices de transición y emisión
        self.trans_matrix = np.ones((self.n_states, self.n_states)) / self.n_states
        self.emit_matrix = np.ones((self.n_states, 3)) / 3

        # Inicializar las probabilidades de estado inicial
        self.init_probs = np.ones(self.n_states) / self.n_states

        # Llevar el registro de las conjeturas anteriores
        self.guess_history = []
        self.correct_letters = {}
        self.starting_words = ["TRACE", "SALET", "CRANE", "SLANT", "SLATE"]  # Palabras iniciales comunes

    def update_model(self, guess_word, feedback):
        """
        Actualiza las probabilidades de transición y emisión basadas en conjeturas previas y feedback.
        :param guess_word: Palabra previamente adivinada.
        :param feedback: Resultado de la palabra adivinada.
        """
        try:
            guess_index = self.states.index(guess_word)
        except ValueError:
            return

        # Actualizar la matriz de emisión basada en el feedback
        for i, status in enumerate(feedback):
            letter = guess_word[i]
            if status == '2':  # Letra correcta y en la posición correcta
                self.emit_matrix[guess_index, 2] += 1
                self.correct_letters[letter] = (2, i)
            elif status == '1':  # Letra correcta pero posición incorrecta
                self.emit_matrix[guess_index, 1] += 1
                if letter not in self.correct_letters or self.correct_letters[letter][0] != 2:
                    self.correct_letters[letter] = (1, i)
            else:  # Letra incorrecta
                self.emit_matrix[guess_index, 0] += 1
                if letter not in self.correct_letters:
                    self.correct_letters[letter] = (0, i)

        # Normalizar la matriz de emisión
        self.emit_matrix[guess_index, :] /= np.sum(self.emit_matrix[guess_index, :])

        # Actualizar la matriz de transición
        if self.guess_history:
            prev_guess_word = self.guess_history[-1]
            prev_guess_index = self.states.index(prev_guess_word)
            self.trans_matrix[prev_guess_index, guess_index] += 1

        # Normalizar la matriz de transición
        for i in range(self.n_states):
            self.trans_matrix[i, :] /= np.sum(self.trans_matrix[i, :])

        # Registrar la palabra adivinada
        self.guess_history.append(guess_word)

    def is_valid_guess(self, word):
        """
        Verifica si una palabra es válida basándose en letras correctas e incorrectas.
        :param word: La palabra para verificar.
        :return: True si es válida, False en caso contrario.
        """
        for letter, (status, index) in self.correct_letters.items():
            if status == 2 and (index >= len(word) or word[index] != letter):
                return False
            elif status == 1 and (letter not in word or word[index] == letter):
                return False
            elif status == 0 and letter in word:
                return False
        return True

    def guess(self) -> str:
        """
        The agent tries to guess the word based on the model.
        :return: The agent's guess
        """
        # Excluir palabras ya intentadas
        previous_guesses = set([g[0] for g in self.guess_history])
        
        if not self.guess_history:
            # Elegir una palabra inicial entre las opciones comunes que no se haya intentado
            valid_starting = [word for word in self.starting_words if word not in previous_guesses]
            if valid_starting:
                return choice(valid_starting)
            else:
                return choice(self.states)

        # Filtrar palabras válidas basadas en letras correctas e incorrectas
        valid_guesses = [word for word in self.states if word not in previous_guesses and self.is_valid_guess(word)]

        if valid_guesses:
            return choice(valid_guesses)
        else:
            # Si no hay palabras válidas, elegir una palabra al azar que no se haya intentado
            untried_words = [word for word in self.states if word not in previous_guesses]
            if untried_words:
                return choice(untried_words)
            else:
                return choice(self.states)
