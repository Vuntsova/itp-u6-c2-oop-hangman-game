from .exceptions import *
import random

class GuessAttempt(object):
    def __init__(self, letter = None, hit = None, miss = None):
        self.letter = letter
        self.hit = hit
        self.miss = miss
        
        if self.hit == True and self.miss == True:
            raise InvalidGuessAttempt()


    def is_hit(self):
        return bool(self.hit)

    def is_miss(self):
        return bool(self.miss)


class GuessWord(object):
    def __init__(self, word):
        if not word:
            raise InvalidWordException()
        self.answer = word.lower()
        self.masked = "*" * len(word)

    def perform_attempt(self, guess):
        guess = guess.lower()
        if len(guess) > 1:
            raise InvalidGuessedLetterException()

        if guess not in self.answer:
            return GuessAttempt(guess, miss=True)

        
        else:
            
            pos = [p for p, char in enumerate(self.answer) if char == guess]
            
            for i in pos:
                self.masked = self.masked[:i] + guess + self.masked[(i + 1):]

        return GuessAttempt(guess, hit=True)

class HangmanGame(object):

    WORD_LIST = ['rmotr', 'python', 'awesome']

    def __init__(self, word_list = None, number_of_guesses = 5):
        if not word_list:
            word_list = self.WORD_LIST
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []
        answer = self.select_random_word(word_list)
        self.word = GuessWord(answer)
        # self.word =

    @classmethod
    def select_random_word(cls, word_list):
        if not word_list:
            raise InvalidListOfWordsException('List must have items')
        return random.choice(word_list)


    def is_finished(self):
        if self.word.masked == self.word.answer or self.remaining_misses == 0:
            return True
        else:
            return False

    def is_won(self):
        if self.word.masked == self.word.answer:
            return True
        else:
            return False

    def is_lost(self):
        if self.remaining_misses == 0:
            return True
        else:
            return False


    def guess(self, guess):
        
        if self.is_finished():
            raise GameFinishedException()

        if guess in self.previous_guesses:
            raise InvalidGuessAttempt()    

        self.previous_guesses.append(guess.lower())

        attempt = self.word.perform_attempt(guess)

        if attempt.is_miss() == True:
            self.remaining_misses -= 1

        if self.is_won():
            raise GameWonException()
        if self.is_lost():
            raise GameLostException()

        return attempt