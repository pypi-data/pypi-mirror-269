import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# Load the dataset
df = pd.read_csv('Churn_Modelling.csv')

# Display class distribution
class_counts = df['Exited'].value_counts()
print(class_counts)

# Visualize class distribution
sns.countplot(x='Exited', data=df)
plt.title('Class Distribution')
plt.xlabel('Class Label')
plt.ylabel('Number of Examples')
plt.show()

# Splitting the data with stratification
X_train, X_test, y_train, y_test = train_test_split(df[['CreditScore', 'Age']], df['Exited'], test_size=0.2, stratify=df['Exited'], random_state=101)

# Define the SMOTE object
smote = SMOTE(random_state=101)

# Resample the training data
X_oversample, y_oversample = smote.fit_resa
