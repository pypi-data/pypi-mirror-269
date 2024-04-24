import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

# Load the dataset from the provided file
file_path = "california_housing_train.csv"
df = pd.read_csv(file_path)

# Display the first few rows of the dataset
print("First few rows of the dataset:")
print(df.head())

# Summary statistics
print("\nSummary statistics:")
print(df.describe())

# Normal distribution
sns.histplot(df['median_house_value'], kde=True, color='blue')
plt.title('Distribution of Housing Prices (Normal)')
plt.xlabel('Price')
plt.ylabel('Frequency')
plt.show()

# Poisson distribution
# Generate Poisson distributed data
poisson_data = np.random.poisson(lam=5, size=1000)
sns.histplot(poisson_data, kde=True, color='green')
plt.title('Poisson Distribution')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.show()

# Confidence Interval
confidence_interval = stats.norm.interval(0.95, loc=np.mean(df['median_house_value']), scale=np.std(df['median_house_value']))
print("\nConfidence Interval for the mean of housing prices (95%):", confidence_interval)

# Z-test
mean_price = df['median_house_value'].mean()
std_price = df['median_house_value'].std()
n = len(df['median_house_value'])
z_stat = (mean_price - 3) / (std_price / np.sqrt(n))
p_value = 1 - stats.norm.cdf(z_stat)
print("\nZ-test:")
print("Z-statistic:", z_stat)
print("P-value:", p_value)

# T-test
t_stat, p_value = stats.ttest_1samp(df['median_house_value'], popmean=3)
print("\nT-test:")
print("T-statistic:", t_stat)
print("P-value:", p_value)

# Example: One-way ANOVA (hypothetical)
df['region'] = np.random.choice(['A', 'B', 'C'], size=len(df))
grouped_data = df.groupby('region')['median_house_value'].apply(list)
f_stat, p_value = stats.f_oneway(*grouped_data)
print("\nANOVA:")
print("F-statistic:", f_stat)
print("P-value:", p_value)
