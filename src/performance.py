import csv
import time
import statistics
from game.wordle import Wordle
from models.constraints.constraints import Constraints
from models.minimax.minimax import Minimax

def testAlgorithm(agent_class, agent_name, answersPath, guessesPath, trialsNumber=100):
    results = []
    
    for _ in range(trialsNumber):
        game = Wordle(answersPath, guessesPath)
        game.set_agent(agent_class())
        
        starting = time.time()
        game.play()
        ending = time.time()
        
        result = {
            'model': agent_name,
            'totalTime': ending - starting,
            'attempts': len([guess for guess in game.user_guesses if guess]),
            'answerWord': game.answer,
            'guessWords': game.user_guesses,
            'won': game.has_won
        }
        results.append(result)

    # Calcula promedios y tasas
    avgTime = statistics.mean([res['totalTime'] for res in results])
    avgAttempts = statistics.mean([res['attempts'] for res in results])
    accuracy = (sum([1 for res in results if res['won']]) / trialsNumber) * 100
    
    summary = {
        'averageTime': avgTime,
        'averageAttempts': avgAttempts,
        'accuracy': accuracy,
        'failureRate': 100 - accuracy
    }
    results.append(summary)
    
    return results

def saveResults(results, filename):
    keys = results[0].keys()
    with open(filename, 'w', newline='') as output_file:
        dictWriter = csv.DictWriter(output_file, keys)
        dictWriter.writeheader()
        for result in results:
            dictWriter.writerow(result)

if __name__ == "__main__":
    constraintsResults = testAlgorithm(Constraints, 'Constraints', 'src/data/answers.txt', 'src/data/guesses.txt', 100)
    saveResults(constraintsResults, 'src/results/constraintsPerformance.csv')
    minimaxResults = testAlgorithm(Minimax, 'Minimax', 'src/data/answers.txt', 'src/data/guesses.txt', 100)
    saveResults(minimaxResults, 'src/results/minimaxPerformance.csv')

    print("Results saved up in respective CSV files")