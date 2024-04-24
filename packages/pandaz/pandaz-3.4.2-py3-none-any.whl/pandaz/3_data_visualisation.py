import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

file_path = 'california_housing_train.csv'
df = pd.read_csv(file_path)

print("Dataset printed for testing: \n")
print(df)

# Histogram
plt.figure(figsize=(8, 6))
sns.histplot(df['median_house_value'], kde=True, color='skyblue')
plt.title('Histogram of Median House Value')
plt.xlabel('Median House Value')
plt.ylabel('Frequency')
plt.show()

# Bar chart
plt.figure(figsize=(8, 6))
sns.countplot(x='population', data=df, palette='pastel')
plt.title('Bar Chart using Population and Count')
plt.xlabel('Population')
plt.ylabel('Count')
plt.show()

# Quartile plot
plt.figure(figsize=(8, 6))
sns.boxplot(y=df['housing_median_age'], color='lightblue')
plt.title('Quartile Plot of Housing Median Age')
plt.ylabel('Housing Median Age')
plt.show()

# Distribution chart
plt.figure(figsize=(8, 6))
sns.histplot(df['total_rooms'], kde=True, color='lightgreen', stat='density')
plt.title('Distribution Chart of Total Rooms')
plt.xlabel('Total Rooms')
plt.ylabel('Density')
plt.show()

# Scatterplot
plt.figure(figsize=(8, 6))
sns.scatterplot(x='median_income', y='median_house_value', data=df)
plt.title('Scatterplot of Median Income vs Median House Value')
plt.xlabel('Median Income')
plt.ylabel('Median House Value')
plt.show()

# Scatter Matrix
sns.pairplot(df.sample(n=1000), vars=['median_income', 'housing_median_age', 'total_rooms', 'median_house_value'], palette='husl')
plt.suptitle('Scatter Matrix of California Housing Dataset', y=1.02)
plt.show()

# Bubblechart
plt.figure(figsize=(10, 8))
plt.scatter(df['longitude'], df['latitude'], s=df['population']/100, c=df['median_house_value'], cmap='cool', alpha=0.5)
plt.colorbar(label='Median House Value')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Bubble Chart of Geographic Distribution and Population')
plt.grid(True)
plt.show()

# Density Chart
plt.figure(figsize=(8, 6))
sns.kdeplot(x=df['median_income'], y=df['median_house_value'], cmap="Blues", shade=True)
plt.title('Density Chart of Median Income vs Median House Value')
plt.xlabel('Median Income')
plt.ylabel('Median House Value')
plt.show()

# Heat map
plt.figure(figsize=(10, 8))
corr_matrix = df.corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title('Heatmap of Correlation Matrix')
plt.show()
