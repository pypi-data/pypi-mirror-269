import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors, LocalOutlierFactor
from scipy.stats.mstats import winsorize

# Load the dataset
file_path = 'california_housing_train.csv'
df = pd.read_csv(file_path)

# Normalize the data
X = df.drop(['median_house_value'], axis=1)
X = (X - X.mean()) / X.std()

# Visual analysis using distplot, boxplots, scatter plots
plt.figure(figsize=(10, 6))
sns.histplot(df['median_house_value'], kde=True, color='skyblue')
plt.title('Distribution of Median House Value')
plt.xlabel('Median House Value')
plt.ylabel('Frequency')
plt.show()

plt.figure(figsize=(8, 6))
sns.boxplot(y=df['median_house_value'], color='lightblue')
plt.title('Boxplot of Median House Value')
plt.ylabel('Median House Value')
plt.show()

plt.figure(figsize=(8, 6))
plt.scatter(df['longitude'], df['latitude'], alpha=0.5)
plt.title('Scatter Plot of Longitude vs Latitude')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()

# Outlier detection using KNN
knn_model = NearestNeighbors(n_neighbors=5)
knn_model.fit(X)
distances, indices = knn_model.kneighbors(X)
outlier_scores = distances.mean(axis=1)

plt.figure(figsize=(8, 6))
plt.plot(outlier_scores)
plt.title('Outlier Scores (K-NN)')
plt.xlabel('Sample Index')
plt.ylabel('Outlier Score')
plt.show()

# Outlier detection using LOF
lof_model = LocalOutlierFactor(n_neighbors=20, contamination=0.1)
lof_labels = lof_model.fit_predict(X)

plt.figure(figsize=(8, 6))
plt.scatter(df['longitude'], df['latitude'], c=lof_labels, cmap='coolwarm', alpha=0.5)
plt.title('Outlier Detection using LOF')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()

# Winsorization
trimmed_values = winsorize(df['median_house_value'], limits=[0.05, 0.05])

plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
sns.histplot(trimmed_values, kde=True, color='skyblue')
plt.title('Distribution after Winsorization')
plt.xlabel('Median House Value')
plt.ylabel('Frequency')

plt.subplot(1, 2, 2)
sns.boxplot(y=trimmed_values, color='lightblue')
plt.title('Boxplot after Winsorization')
plt.ylabel('Median House Value')
plt.tight_layout()
plt.show()
