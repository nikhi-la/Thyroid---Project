# -*- coding: utf-8 -*-
"""sample.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1WQIRquS4K5sqsypRRw7gF01nds9cAYDQ

# Load Dataset
"""

import pandas as pd

df = pd.read_csv("/content/drive/MyDrive/Thyroid/thyroidDF.csv")
df

"""# Data Preprocessing

**Check for missing values**
"""

missing_values = df.isnull().sum()
missing_values

"""* sex has 307 missing values
* TSH has	842 missing values
* T3 has 2604 missing values
* TT4 has 442 missing values
* T4U has 809 missing values
* FTI has 802 missing values
* TBG has 8823 missing values

**Remove rows with significant missing data**

* remove column which has more than 3000 missing values ie. TBG
"""

df = df.dropna(axis=1, thresh=len(df) - 3000)
df

""" **Fill missing numerical values and Catgorical values**"""

df['TSH'].fillna(df['TSH'].mean(), inplace=True)
df['T3'].fillna(df['T3'].mean(), inplace=True)
df['TT4'].fillna(df['TT4'].mean(), inplace=True)
df['T4U'].fillna(df['T4U'].mean(), inplace=True)
df['FTI'].fillna(df['FTI'].mean(), inplace=True)

df['sex'].fillna(df['sex'].mode()[0], inplace=True)

df

"""**Converting into numerical data**"""

df['sex'] = df['sex'].map({'M': 1, 'F': 0})

binary_columns = ['on_thyroxine', 'query_on_thyroxine', 'on_antithyroid_meds', 'sick', 'pregnant', 'thyroid_surgery',
                  'I131_treatment', 'query_hypothyroid', 'query_hyperthyroid', 'lithium', 'goitre', 'tumor',
                  'hypopituitary', 'psych', 'TSH_measured', 'T3_measured', 'TT4_measured', 'T4U_measured',
                  'FTI_measured', 'TBG_measured']

for col in binary_columns:
    df[col] = df[col].map({'t': 1, 'f': 0})

df

"""**Remove unnecessary columns 'referral_source' and 'patient_id'**"""

df.drop(columns=['referral_source', 'patient_id'], inplace=True)
df.info()

"""**remove duplicates**"""

df = df.drop_duplicates()
df

"""**Showing outliers**"""

import matplotlib.pyplot as plt
import seaborn as sns

# Set up the matplotlib figure
plt.figure(figsize=(16, 12))

# List of numerical features to visualize
numerical_features = ['age', 'TSH', 'T3', 'TT4', 'T4U', 'FTI']

# Create a box plot for each numerical feature
for i, feature in enumerate(numerical_features, 1):
    plt.subplot(3, 3, i)
    sns.boxplot(data=df, x=feature)
    plt.title(f'Box plot of {feature}')

plt.tight_layout()
plt.show()

"""**Analyze target class distribution**"""

class_distribution = df['target'].value_counts()
class_distribution

class_percentage = df['target'].value_counts(normalize=True) * 100
class_percentage

"""**Classify under no thyroid and thyroid**"""

def classify_thyroid(condition):
    if condition=='-':  # Replace with actual class names
        return 'no thyroid'
    else:
        return 'thyroid'

# Apply the classification function
df['target'] = df['target'].apply(classify_thyroid)
df['target'].value_counts()

df

"""#Resampling-Oversampling"""

from imblearn.over_sampling import RandomOverSampler

X = df.drop('target', axis=1)  # Replace 'target_column' with the actual name of your target column
y = df['target']
# Define the oversampler
ros = RandomOverSampler(random_state=42)

# Resample the data
X_res, y_res = ros.fit_resample(X, y)

# Check the class distribution
#print(y_res.value_counts())
df = pd.concat([X_res, y_res], axis=1)
df

"""#Feature selection

**using univariate feature selection**
"""

from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, f_classif

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

feature_scores = pd.DataFrame({'Feature': X.columns, 'Score': selector.scores_})
feature_scores = feature_scores.sort_values(by='Score', ascending=False)

#score of each feature
feature_scores

#selection of 9 features with top scores
k = 9  # Number of top features to select
selector = SelectKBest(score_func=f_classif, k=k)
X_new = selector.fit_transform(X_train, y_train)

# Get the selected feature names
selected_features = X.columns[selector.get_support()]
selected_features

#use only selected features
X_train_selected = X_train[selected_features]
X_test_selected = X_test[selected_features]

X_train_selected
#X_test_selected

"""#Train the model using random forest

**Accuracy and report**
"""

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Train a Random Forest model
rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X_train_selected, y_train)

# Make predictions
y_pred = rf_model.predict(X_test_selected)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

#accuracy
report

"""# Confusion Matrix"""

from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
# Compute and display the confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred, labels=['no thyroid', 'thyroid'])  # Replace with actual labels if different

plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=['no thyroid', 'thyroid'], yticklabels=['no thyroid', 'thyroid'])
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.title('Confusion Matrix')
plt.show()

"""# Saving the trained Model

*   save as model.pkl
*   save as scaler.pkl
"""

import pickle

from sklearn.preprocessing import StandardScaler


# Assuming you have a trained model
model = RandomForestClassifier()
model.fit(X_train_selected, y_train)  # Train your model

# Save the model to a file
with open('/content/drive/MyDrive/Thyroid/model.pkl','wb') as file:
    pickle.dump(model, file)

# Create and fit the scaler
scaler = StandardScaler()
scaler.fit(X_train_selected)

# Save the scaler to a file
with open('/content/drive/MyDrive/Thyroid/scaler.pkl', 'wb') as file:
    pickle.dump(scaler, file)


#to find the model
import os

# List files in the directory
print(os.listdir('/content/drive/MyDrive/Thyroid/'))