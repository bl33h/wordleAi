import csv
import time
import statistics
from game.wordle import Wordle
from models.bn.bn import BN
from models.hmm.hmm import HMM

def testAlgorithm(agent_class, answersPath, guessesPath, trialsNumber=100):
    totalAttemptss = []
    successes = 0
    totalTime = 0

    for _ in range(trialsNumber):
        game = Wordle(answersPath, guessesPath)
        game.set_agent(agent_class())

        starting = time.time()
        game.play()
        ending = time.time()

        totalTime += ending - starting
        attempts = len([guess for guess in game.user_guesses if guess])
        totalAttemptss.append(attempts)

        if game.has_won:
            successes += 1

    avgAttempts = statistics.mean(totalAttemptss)
    accuracy = (successes / trialsNumber) * 100
    avgTime = totalTime / trialsNumber

    return {
        'averageTime': avgTime,
        'averageAttempts': avgAttempts,
        'accuracy': accuracy,
        'failureRate': 100 - accuracy
    }

def saveResults(results, filename):
    keys = results[0].keys()
    with open(filename, 'w', newline='') as output_file:
        dictWriter = csv.DictWriter(output_file, keys)
        dictWriter.writeheader()
        dictWriter.writerows(results)

if __name__ == "__main__":
    bnResults = testAlgorithm(BN, 'src/data/answers.txt', 'src/data/guesses.txt', 100)
    # hmmResults = testAlgorithm(HMM, 'src/data/answers.txt', 'src/data/guesses.txt', 100)
    saveResults([bnResults], 'src/tests/performance.csv')
    # saveResults([hmmResults], 'performance2.csv')

    print("Results saved up in 'performance.csv'")