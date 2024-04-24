import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, adjusted_mutual_info_score, silhouette_score

# Load the dataset
file_path = 'california_housing_train.csv'
df = pd.read_csv(file_path)

# Prepare data for clustering
X = df.drop('median_house_value', axis=1)

# Formula to normalize data
X = (X - X.mean()) / X.std()

# Define the number of clusters
n_clusters = 3

# Initialize and fit KMeans model
kmeans = KMeans(n_clusters, random_state=42)
kmeans.fit(X)

# Get cluster labels
cluster_labels = kmeans.labels_

print(cluster_labels)

# Evaluate clustering performance
rand_index = adjusted_rand_score(df['median_house_value'], cluster_labels)
print("Rand Index:", rand_index)

mutual_info = adjusted_mutual_info_score(df['median_house_value'], cluster_labels)
print("Mutual Information:", mutual_info)

silhouette_coefficient = silhouette_score(X, cluster_labels)
print("Silhouette Coefficient:", silhouette_coefficient)
