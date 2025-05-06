# preprocessing.py

import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Step 1: Load the dataset
data = pd.read_csv('mental_health_data.csv')

# Step 2: Check for missing values
missing_values = data.isnull().sum()
print("Missing values in each column:")
print(missing_values)

# Step 3: Handle Missing Values
# Handle numeric columns: fill missing values with the mean
numeric_columns = data.select_dtypes(include='number').columns
data[numeric_columns] = data[numeric_columns].fillna(data[numeric_columns].mean())

# Handle categorical columns: fill missing values with the mode (most frequent value)
categorical_columns = data.select_dtypes(include='object').columns
for column in categorical_columns:
    data[column] = data[column].fillna(data[column].mode()[0])

# After handling missing values
print("Missing values after handling:")
print(data.isnull().sum())

# Step 4: Encode categorical columns
label_encoders = {}

for column in data.columns:
    if data[column].dtype == 'object':
        # Initialize a LabelEncoder
        le = LabelEncoder()
        # Fit and transform the column
        data[column] = le.fit_transform(data[column])
        # Save the encoder for future use
        label_encoders[column] = le

# Step 5: Save the processed data
data.to_csv('mental_health_data_processed.csv', index=False)
print("✅ Preprocessing completed: Saved 'mental_health_data_processed.csv'")

# Step 6: Save the label encoders for future use
import pickle
with open('label_encoders.pkl', 'wb') as f:
    pickle.dump(label_encoders, f)
print("✅ Saved label encoders as 'label_encoders.pkl'")
