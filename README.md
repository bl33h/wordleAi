# wordleAi
This project is designed to simulate the Wordle game, where players guess a five-letter word within six tries. The project includes two solving models: Constraints and Minimax, to analyze their performance in solving the game.

<p align="center">
  <br>
  <img src="https://i.giphy.com/62HRHz7zZZYThhTwEI.webp" alt="wb" width="400">
  <br>
</p>
<p align="center" >
  <a href="#features">Features</a> •
  <a href="#Files">Files</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#packages">Packages</a>  • 
  <a href="#packages">References</a>  
</p>

## Features
- **Wordle Game Simulation**: Play the Wordle game with a maximum of 6 guesses.
- **Constraints Model**: Uses constraint satisfaction techniques to solve the game.
- **Minimax Model**: Implements the Minimax algorithm for optimal solution finding.
- **Performance Analysis**: Visualize and compare the success rate, total time, and accuracy of different models.
- **Graphical Representations**: Generate graphs to compare model performances.

## Files
- main.py: The main entry point of the project. It initializes the Wordle game and allows the user to play or run simulations with different solving models.
- wordle.py: Contains the core logic for the Wordle game, including initializing the game, processing guesses, and determining win/loss conditions.
- answers.txt: Contains the list of possible answers for the Wordle game.
- guesses.txt: Contains the list of possible guesses for the Wordle game.
- agent.py: Defines the agent that interacts with the Wordle game, making guesses and receiving feedback.
- state.py: Manages the state of the Wordle game, including the current guesses, remaining attempts, and whether the game has been won or lost.
- file_functions.py: Contains functions for reading and writing to files, primarily used for loading word lists and saving game results.
- feedback.py: Handles the feedback mechanism, providing hints based on the player's guesses and the actual word.
- minimax.py: Implements the Minimax algorithm, a decision-making algorithm used for finding the optimal solution in the Wordle game.
- constraints.py: Implements the Constraints model, which uses constraint satisfaction techniques to solve the Wordle game by narrowing down possible words based on given feedback.
- performance.py: Contains functions to measure the performance of the solving models. It compares success rates, total solving time, and accuracy.
- graphs.py: Generates various graphs to visualize the performance of different solving models. This includes histograms for total time distribution and bar charts for success rates and accuracy.

## Packages
The project requires the following Python packages:
- pandas: For data manipulation and analysis.
- matplotlib: For creating static, animated, and interactive visualizations.
- seaborn: For making statistical graphics.
- numpy: For supporting large, multi-dimensional arrays and matrices.
- scipy: For scientific and technical computing.
  
You can install these packages using the following command:
```
$ pip install pandas matplotlib seaborn numpy scipy
```

## How To Use
To clone and run this application, you'll need [Git](https://git-scm.com) and [Python](https://www.python.org/downloads/) installed on your computer. From your command line:

```
# Clone this repository
$ git clone https://github.com/bl33h/wordleAi

# Open the project
$ cd src

# Run the app
$ python main.py
```
## References
The information located in src/data was retrieved from the [roget repository](https://github.com/jonhoo/roget/tree/main)
