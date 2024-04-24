# Importing necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import statsmodels.api as sm

# Reading the data
# file_path = 'california_housing_train.csv'
df = pd.read_csv('california_housing_train.csv')
print(df)


# Mean
mean = df.mean()
print("Mean: \n", mean)
print("\n\n\n\n")

# Median
median = df.median()
print("Median: ", median)
print("\n\n\n\n")

# Mode
mode = df.mode().iloc[0]
print("Mode: ", mode)
print("\n\n\n\n")

# Minimum
minimum = df.min()
print("Minimum: ", minimum)
print("\n\n\n\n")

# Maximum
maximum = df.max()
print("Maximum: ", maximum)
print("\n\n\n\n")

# Total sum
total_sum = df.sum()
print("Total Sum: ", total_sum)
print("\n\n\n\n")

# Range
range_ = maximum - minimum
print("Range: ", range_)
print("\n\n\n\n")

# First quartile
first_quartile = df.quantile(0.25)
print("First quartile: ", first_quartile)
print("\n\n\n\n")

# Third quartile
third_quartile = df.quantile(0.75)
print("Third quartile: ", third_quartile)
print("\n\n\n\n")

# Interquartile range
iqr = third_quartile - first_quartile
print("IQR: ", iqr)
print("\n\n\n\n")

# Standard Deviation
std_dev = df.std()
print("Standard Deviation: ", std_dev)
print("\n\n\n\n")

# Variance
variance = df.var()
print("Variance: ", variance)
print("\n\n\n\n")

# Correlation
correlation = df.corr()
print("Correlation: ", correlation)
print("\n\n\n\n")

# Mean Standard Error
se_mean = df.sem()
print("Mean Standard Error: ", se_mean)
print("\n\n\n\n")

# Coefficient of variation
coefficient_of_variation = std_dev / mean
print("Coeff of Variation: ", coefficient_of_variation)
print("\n\n\n\n")

# Cells having missing value symbol [N Missing]
n_missing = df.isnull().sum()
print("N Missing: ", n_missing)
print("\n\n\n\n")

# Total Cells
n_total = df.shape[0]
print("n_total: ", n_total)
print("\n\n\n\n")

# Cumulative n
cumulative_n = df.cumsum()
print("Cumulative N: ", cumulative_n)
print("\n\n\n\n")

percent = (df.rank(pct=True) * 100)
print("Percent: ", percent)
print("\n\n\n\n")

cumulative_percent = (df.rank(pct=True, ascending=False) * 100)
print("Cumulative Percent: ", cumulative_percent)
print("\n\n\n\n")

trimmed_mean = df.mean()
print("Trimmed Mean: ", trimmed_mean)
print("\n\n\n\n")

sum_of_squares = (df ** 2).sum()
print("Sum of Squares: ", sum_of_squares)
print("\n\n\n\n")

skewness = df.skew()
print("Skewness: ", skewness)
print("\n\n\n\n")

kurtosis = df.kurtosis()
print("Kurtosis: ", kurtosis)
print("\n\n\n\n")

# Box-and-Whisker Plot
plt.figure(figsize=(10, 6))
sns.boxplot(df)
plt.title('Box-and-Whisker Plot')
plt.show()

# Scatter Matrix
sns.pairplot(df)
plt.title('Scatter Matrix')
plt.show()

# Correlation Matrix
plt.figure(figsize=(10, 8))
sns.heatmap(correlation, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()

# Distributions
# Normal Distribution
normal_distribution = stats.norm.fit(df)
print("Normal Distribution Parameters (mean, std_dev):", normal_distribution)
print("\n\n\n")

# Poisson Distribution
lambda_value = df['longitude'].mean()
poisson_distribution = stats.poisson(mu=lambda_value)
print("Poisson Distribution (Lambda):", lambda_value)
print("\n\n\n")

# Population Parameters
population_mean = df.mean()
population_std_dev = df.std()
print("Population Mean:", population_mean)
print("\n\n\n")
print("Population Standard Deviation:", population_std_dev)
print("\n\n\n")

sample = df.sample(n=100)
sample_mean = sample.mean()
sample_std_dev = sample.std()
standard_error = sample_std_dev / np.sqrt(len(sample))
print("Sample Mean:", sample_mean)
print("\n\n\n")
print("Sample Standard Deviation:", sample_std_dev)
print("\n\n\n")
print("Standard Error:", standard_error)
print("\n\n\n")
confidence_interval = stats.norm.interval(0.95, loc=sample_mean, scale=standard_error)
print("Confidence Interval (95%):", confidence_interval)
print("\n\n\n")

# Z-test
z_statistic, p_value_z = sm.stats.ztest(sample, value=population_mean)
print("Z-test Statistic:", z_statistic)
print("\n\n\n")
print("p-value (Z-test):", p_value_z)
print("\n\n\n")

# t-test
sample_2 = df.sample(n=100)
t_statistic, p_value_t = stats.ttest_ind(sample, sample_2)
print("t-test Statistic:", t_statistic)
print("\n\n\n")
print("p-value (t-test):", p_value_t)
print("\n\n\n")
