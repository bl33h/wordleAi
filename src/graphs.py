import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

path = 'src/results/'

# load data from CSV files
constraintsPerformance = pd.read_csv(path + 'constraintsPerformance.csv')
minimaxPerformance = pd.read_csv(path + 'minimaxPerformance.csv')
constraintsSummary = pd.read_csv(path + 'constraintsSummary.csv')
minimaxSummary = pd.read_csv(path + 'minimaxSummary.csv')

# combine both performance datasets for easier visualization
combinedPerformance = pd.concat([constraintsPerformance, minimaxPerformance])

# histogram for total time distribution by model
plt.figure(figsize=(10, 6))
sns.histplot(data=combinedPerformance, x='totalTime', hue='model', element='step', stat='density', common_norm=False)
plt.title('Distribution of Total Time by Model')
plt.xlabel('Total Time')
plt.ylabel('Density')
plt.show()

# calculating success rate
successRate = combinedPerformance.groupby('model')['won'].mean() * 100

plt.figure(figsize=(8, 6))
successRate.plot(kind='bar', color=['purple', 'pink'])
plt.title('Success Rate by Model')
plt.xlabel('Model')
plt.ylabel('Success Rate (%)')
plt.ylim(0, 100)
plt.show()

models = ['Constraints', 'Minimax']
averageTimes = [constraintsSummary['averageTime'].iloc[0], minimaxSummary['averageTime'].iloc[0]]

# bar chart for average time comparison
plt.figure(figsize=(8, 5))
plt.bar(models, averageTimes, color=['purple', 'pink'])
plt.title('Average Time Comparison by Model')
plt.xlabel('Model')
plt.ylabel('Average Time')
plt.show()

accuracies = [constraintsSummary['accuracy'].iloc[0], minimaxSummary['accuracy'].iloc[0]]

# bar chart for accuracy comparison
plt.figure(figsize=(8, 5))
plt.bar(models, accuracies, color=['purple', 'pink'])
plt.title('Accuracy Comparison by Model')
plt.xlabel('Model')
plt.ylabel('Accuracy (%)')
plt.ylim(0, 100)
plt.show()