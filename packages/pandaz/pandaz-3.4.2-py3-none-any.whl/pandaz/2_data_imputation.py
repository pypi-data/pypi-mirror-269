# Import necessary libraries
import pandas as pd
from sklearn.impute import KNNImputer

# Load the California housing training dataset
file_path = 'california_housing_train.csv'
df = pd.read_csv(file_path)

# Deletion of rows with missing data
df_notnull = df.dropna()
print("Deletion of rows with missing data:\n", df_notnull)

# Mean imputation
df_mean_imputed = df.fillna(df.mean())
print("\nMean Imputation:\n", df_mean_imputed)

# Median imputation
df_median_imputed = df.fillna(df.median())
print("\nMedian Imputation:\n", df_median_imputed)

# Mode imputation
df_mode_imputed = df.fillna(df.mode().iloc[0])
print("\nMode Imputation:\n", df_mode_imputed)

# Arbitrary value imputation
arbitrary_value = 99999
df_arbitrary_imputed = df.fillna(arbitrary_value)
print("\nArbitrary Value Imputation:\n", df_arbitrary_imputed)

# End of tail imputation
end_of_tail_value = df['total_bedrooms'].mean() + 3 * df['total_bedrooms'].std()  
# Example: Use 3 standard deviations from the mean
df_end_of_tail_imputed = df.fillna(end_of_tail_value)
print("\nEnd of Tail Imputation:\n", df_end_of_tail_imputed)

# Random sample imputation
random_sample = df['total_bedrooms'].dropna().sample(df['total_bedrooms'].isnull().sum(), random_state=42)
df_random_sample_imputed = df.copy()
df_random_sample_imputed.loc[df['total_bedrooms'].isnull(), 'total_bedrooms'] = random_sample.values
print("\nRandom Sample Imputation:\n", df_random_sample_imputed)


# Frequent category imputation
frequent_category = df['total_rooms'].mode()[0]
df_frequent_category_imputed = df.fillna({'total_rooms': frequent_category})
print("\nFrequent Category Imputation:\n", df_frequent_category_imputed)

# Adding a new category as "Missing"
df_missing_category_imputed = df.fillna({'total_rooms': 'Missing'})
print("\nMissing Category Imputation:\n", df_missing_category_imputed)

# Regression imputation
knn_imputer = KNNImputer()
df_regression_imputed = pd.DataFrame(knn_imputer.fit_transform(df), columns=df.columns)
print("\nRegression Imputation:\n", df_regression_imputed)
