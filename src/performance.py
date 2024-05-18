import csv
import time
import statistics
from game.wordle import Wordle
from models.minimax.minimax import Minimax
from models.constraints.constraints import Constraints

def testAlgorithm(agent_class, agent_name, answersPath, guessesPath, trialsNumber=100):
    results = []
    
    for i in range(trialsNumber):
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

        if (i + 1) % 10 == 0:
            print(f'\n---------------------- [{i + 1}] completed iterations so far ----------------------')

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
            if 'model' in result:
                dictWriter.writerow(result)

def saveSummary(summary, filename):
    keys = summary.keys()
    with open(filename, 'w', newline='') as output_file:
        dictWriter = csv.DictWriter(output_file, keys)
        dictWriter.writeheader()
        dictWriter.writerow(summary)

if __name__ == "__main__":
    constraintsResults = testAlgorithm(Constraints, 'Constraints', 'src/data/answers.txt', 'src/data/guesses.txt', 2310)
    minimaxResults = testAlgorithm(Minimax, 'Minimax', 'src/data/answers.txt', 'src/data/guesses.txt', 2310)
    
    saveResults(constraintsResults[:-1], 'src/results/constraintsPerformance.csv')
    saveResults(minimaxResults[:-1], 'src/results/minimaxPerformance.csv')
    
    saveSummary(constraintsResults[-1], 'src/results/constraintsSummary.csv')
    saveSummary(minimaxResults[-1], 'src/results/minimaxSummary.csv')

    print("Results and summaries saved up in respective CSV files")