# train_model.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import RandomForestRegressor
import pickle

# Step 1: Load the preprocessed data
data = pd.read_csv('mental_health_data_processed.csv')

# Step 2: Define the features (X) and targets (y)
X = data.drop(columns=['user_id', 'depression_percent', 'anxiety_percent', 'stress_percent', 'suggestion'])
y = data[['depression_percent', 'anxiety_percent', 'stress_percent']]

# Step 3: Split the data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 4: Create and train the model
model = MultiOutputRegressor(RandomForestRegressor(n_estimators=100, random_state=42))
model.fit(X_train, y_train)

# Step 5: Save the trained model
with open('mental_health_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("✅ Model training completed and model saved as 'mental_health_model.pkl'")
