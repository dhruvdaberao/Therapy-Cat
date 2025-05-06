# import pandas as pd
# import pickle

# # Step 1: Load the saved model
# with open('mental_health_model.pkl', 'rb') as f:
#     model = pickle.load(f)

# # Step 2: Load label encoders
# with open('label_encoders.pkl', 'rb') as f:
#     label_encoders = pickle.load(f)

# # Step 3: Identify categorical and numeric columns
# categorical_columns = [
#     'feeling_today', 'eating_healthy', 'exercise_frequency', 
#     'social_support', 'routine_satisfaction', 'recent_happiness', 
#     'relaxation_frequency', 'overwhelmed', 'social_connection', 
#     'emotional_selfcare', 'motivation', 'lifestyle_happiness', 'goal_setting'
# ]

# # Add numeric columns here if necessary
# numeric_columns = [
#     'stress_level', 'sleep_quality', 'exercise_frequency', 'social_support', 
#     'routine_satisfaction', 'recent_happiness', 'relaxation_frequency', 
#     'overwhelmed', 'social_connection', 'motivation', 'lifestyle_happiness', 
#     'goal_setting'
# ]

# # Step 4: Function to preprocess new input
# def preprocess_input(input_data):
#     # input_data is a dictionary
#     df = pd.DataFrame([input_data])

#     # Encode categorical columns
#     for col in categorical_columns:
#         if col in df.columns:
#             if df[col].dtype == 'object':  # Apply LabelEncoder only to object types (categorical columns)
#                 le = label_encoders.get(col)
#                 if le is not None:
#                     # Handle unseen labels gracefully
#                     try:
#                         # If the label is unseen, map it to the most frequent label (fallback)
#                         df[col] = df[col].apply(lambda x: le.transform([x])[0] if x in le.classes_ else le.transform([le.classes_[0]])[0])
#                     except KeyError as e:
#                         # If there's a KeyError (unseen label), map it to a known class
#                         print(f"Warning: Unseen label {e} found in column '{col}'. Using the most frequent label.")
#                         df[col] = df[col].apply(lambda x: le.transform([le.classes_[0]])[0])  # Default to the first class

#     # Ensure numeric columns are treated as numeric (not encoded)
#     for col in numeric_columns:
#         if col in df.columns:
#             df[col] = pd.to_numeric(df[col], errors='coerce')

#     return df

# # Step 5: Predict function
# def predict_mental_health(input_data):
#     processed_data = preprocess_input(input_data)
#     predictions = model.predict(processed_data)
#     return {
#         "depression_percent": round(predictions[0][0], 2),
#         "anxiety_percent": round(predictions[0][1], 2),
#         "stress_percent": round(predictions[0][2], 2)
#     }

# # Step 6: Example usage
# if __name__ == "__main__":
#     example_input = {
#         "feeling_today": "Happy",
#         "stress_level": 3,  # This is a numeric value now, so it should not be encoded
#         "sleep_quality": 7,  # This is a numeric value now, so it should not be encoded
#         "eating_healthy": "Sometimes",
#         "exercise_frequency": "Few times",
#         "social_support": "Sometimes",
#         "routine_satisfaction": "Not satisfied",
#         "recent_happiness": "Family/Friends",
#         "relaxation_frequency": "Rarely",
#         "overwhelmed": "No",
#         "social_connection": "Trying",  # This is a categorical column
#         "emotional_selfcare": "Not motivated",  # Handle unseen label here
#         "motivation": "Somewhat",
#         "lifestyle_happiness": "Maybe",
#         "goal_setting": "Neutral"
#     }

#     prediction = predict_mental_health(example_input)
#     print("🎯 Prediction:", prediction)








# import pandas as pd
# import numpy as np
# from sklearn.preprocessing import LabelEncoder
# from sklearn.ensemble import RandomForestRegressor
# import joblib  # For loading the trained model

# # Step 1: Load the trained model (Assuming it has already been trained and saved)
# model = joblib.load('mental_health_model.pkl')

# # Step 2: Load the Label Encoders for preprocessing
# label_encoders = joblib.load('label_encoders.pkl')  # Loading encoders for categorical columns

# # Step 3: Preprocessing function
# def preprocess_input(input_data):
#     df = pd.DataFrame([input_data])
    
#     # Remove 'user_id' if it exists in the input
#     if 'user_id' in df.columns:
#         df = df.drop(columns=['user_id'])

#     for col in df.columns:
#         if df[col].dtype == 'object':
#             le = label_encoders.get(col)
#             if le:
#                 # Check if value exists in encoder classes
#                 df[col] = df[col].apply(lambda x: x if x in le.classes_ else 'unknown')
#                 # Extend the encoder classes to handle 'unknown'
#                 if 'unknown' not in le.classes_:
#                     le.classes_ = np.append(le.classes_, 'unknown')
#                 df[col] = le.transform(df[col])

#     numerical_cols = df.select_dtypes(include=[np.number]).columns
#     df[numerical_cols] = df[numerical_cols].apply(lambda x: (x - x.mean()) / x.std(), axis=0)
    
#     return df



# # Step 4: Prediction function
# def predict_mental_health(input_data):
#     # Preprocess the input data (Encode categorical features, scale numerical features, etc.)
#     processed_data = preprocess_input(input_data)
    
#     # Get predictions from the model
#     predictions = model.predict(processed_data)
    
#     # Map predictions to the result structure
#     result = {
#         'depression_percent': predictions[0][0],
#         'anxiety_percent': predictions[0][1],
#         'stress_percent': predictions[0][2],
#     }
    
#     return result

# # Step 5: Interpretation and Suggestions Function
# def interpret_and_suggest(prediction):
#     # Unpacking the prediction
#     depression_percent = prediction['depression_percent']
#     anxiety_percent = prediction['anxiety_percent']
#     stress_percent = prediction['stress_percent']
    
#     # Interpretation and suggestions
#     results = {}
    
#     # Depression interpretation and suggestions
#     if depression_percent > 60:
#         results['depression'] = 'High Depression (Consider seeking professional help. Practice mindfulness and self-care.)'
#     elif depression_percent > 30:
#         results['depression'] = 'Moderate Depression (Try maintaining a healthy routine and talking to someone.)'
#     else:
#         results['depression'] = 'Low Depression (Keep up with healthy habits, stay active.)'

#     # Anxiety interpretation and suggestions
#     if anxiety_percent > 60:
#         results['anxiety'] = 'High Anxiety (Consider relaxation techniques, talk to a professional.)'
#     elif anxiety_percent > 30:
#         results['anxiety'] = 'Moderate Anxiety (Engage in physical activity and practice stress management.)'
#     else:
#         results['anxiety'] = 'Low Anxiety (Keep maintaining your healthy habits.)'

#     # Stress interpretation and suggestions
#     if stress_percent > 60:
#         results['stress'] = 'High Stress (Try yoga, exercise, and set aside time for self-care.)'
#     elif stress_percent > 30:
#         results['stress'] = 'Moderate Stress (Take regular breaks, engage in relaxation activities.)'
#     else:
#         results['stress'] = 'Low Stress (Continue maintaining a stress-free routine.)'
    
#     return results

# # Example input data (this should be replaced with real input data)
# example_input = {
#     'user_id': 12345,  # This would be an identifier but is not used for prediction
#     'feeling_today': 'Happy',
#     'stress_level': 5,  # Example stress level (numeric)
#     'sleep_quality': 7,  # Example sleep quality (numeric)
#     'eating_healthy': 8,  # Example eating habits (numeric)
#     'exercise_frequency': 6,  # Example exercise frequency (numeric)
#     'social_support': 7,  # Example social support (numeric)
#     'routine_satisfaction': 7,  # Example routine satisfaction (numeric)
#     'recent_happiness': 8,  # Example recent happiness (numeric)
#     'relaxation_frequency': 6,  # Example relaxation frequency (numeric)
#     'overwhelmed': 2,  # Example overwhelmed level (numeric)
#     'social_connection': 5,  # Example social connection (numeric)
#     'emotional_selfcare': 'Very motivated',  # Example emotional self-care (categorical)
#     'motivation': 7,  # Example motivation level (numeric)
#     'lifestyle_happiness': 8,  # Example lifestyle happiness (numeric)
#     'goal_setting': 7  # Example goal setting (numeric)
# }

# # Make a prediction
# prediction = predict_mental_health(example_input)

# # Interpret the results and provide suggestions
# suggestions = interpret_and_suggest(prediction)

# # Print the suggestions
# print("Suggestions based on predictions:")
# for condition, suggestion in suggestions.items():
#     print(f"{condition.capitalize()}: {suggestion}")



# import matplotlib.pyplot as plt
# import numpy as np

# def plot_predictions(depression, anxiety, stress):
#     # Define categories and colors
#     categories = ['Depression', 'Anxiety', 'Stress']
#     values = [depression, anxiety, stress]
    
#     # Define the threshold ranges (low, medium, high)
#     thresholds = {
#         'low': (0, 20),
#         'medium': (20, 50),
#         'high': (50, 100)
#     }
    
#     # Function to categorize the levels
#     def get_category(value):
#         if value < thresholds['low'][1]:
#             return 'Low', 'green'
#         elif value < thresholds['medium'][1]:
#             return 'Medium', 'yellow'
#         else:
#             return 'High', 'red'

#     # Generate categories and corresponding colors
#     category_labels = []
#     colors = []
#     for value in values:
#         category, color = get_category(value)
#         category_labels.append(category)
#         colors.append(color)
    
#     # Plot
#     fig, ax = plt.subplots()
#     bars = ax.bar(categories, values, color=colors)
    
#     # Add the category labels on top of the bars
#     for bar, category_label in zip(bars, category_labels):
#         height = bar.get_height()
#         ax.text(bar.get_x() + bar.get_width() / 2, height + 1, category_label, 
#                 ha='center', va='bottom', fontsize=12, fontweight='bold')
    
#     # Title and labels
#     ax.set_title('Mental Health Predictions', fontsize=14)
#     ax.set_ylabel('Percentage (%)')
#     ax.set_ylim(0, 100)  # Setting the limit for the Y-axis
    
#     # Display the plot
#     plt.show()

# # Example usage (prediction output from model)
# depression_percent = 34.9
# anxiety_percent = 0.0
# stress_percent = 10.0

# # Plot the results
# plot_predictions(depression_percent, anxiety_percent, stress_percent)



import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Personalized Suggestions based on prediction
def get_suggestions(depression, anxiety, stress):
    suggestions = {}

    # Depression suggestions
    if depression < 20:
        suggestions['depression'] = "Low Depression (Keep up with healthy habits, stay active.)"
    elif depression < 50:
        suggestions['depression'] = "Moderate Depression (Consider socializing more and practicing mindfulness.)"
    else:
        suggestions['depression'] = "High Depression (It's important to talk to a mental health professional.)"
    
    # Anxiety suggestions
    if anxiety < 20:
        suggestions['anxiety'] = "Low Anxiety (Keep maintaining your healthy habits.)"
    elif anxiety < 50:
        suggestions['anxiety'] = "Moderate Anxiety (Try relaxation techniques and balanced routines.)"
    else:
        suggestions['anxiety'] = "High Anxiety (Consider seeing a counselor for anxiety management.)"
    
    # Stress suggestions
    if stress < 20:
        suggestions['stress'] = "Low Stress (Continue maintaining a stress-free routine.)"
    elif stress < 50:
        suggestions['stress'] = "Moderate Stress (Consider taking short breaks and managing time effectively.)"
    else:
        suggestions['stress'] = "High Stress (Prioritize relaxation, try meditation, and speak to a counselor.)"

    return suggestions

# Save predictions and suggestions to a CSV file
def save_results(depression, anxiety, stress, suggestions):
    data = {
        'depression_percent': depression,
        'anxiety_percent': anxiety,
        'stress_percent': stress,
        'depression_suggestion': suggestions['depression'],
        'anxiety_suggestion': suggestions['anxiety'],
        'stress_suggestion': suggestions['stress']
    }

    df = pd.DataFrame([data])
    
    # Save the results to a CSV file
    df.to_csv('mental_health_predictions.csv', mode='a', header=False, index=False)

    print("Results saved to 'mental_health_predictions.csv'")

# Plotting function (unchanged)
def plot_predictions(depression, anxiety, stress):
    categories = ['Depression', 'Anxiety', 'Stress']
    values = [depression, anxiety, stress]
    
    thresholds = {
        'low': (0, 20),
        'medium': (20, 50),
        'high': (50, 100)
    }
    
    def get_category(value):
        if value < thresholds['low'][1]:
            return 'Low', 'green'
        elif value < thresholds['medium'][1]:
            return 'Medium', 'yellow'
        else:
            return 'High', 'red'

    category_labels = []
    colors = []
    for value in values:
        category, color = get_category(value)
        category_labels.append(category)
        colors.append(color)
    
    fig, ax = plt.subplots()
    bars = ax.bar(categories, values, color=colors)
    
    for bar, category_label in zip(bars, category_labels):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 1, category_label, 
                ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    ax.set_title('Mental Health Predictions', fontsize=14)
    ax.set_ylabel('Percentage (%)')
    ax.set_ylim(0, 100)
    
    plt.show()

# Example predictions
depression_percent = 34.9
anxiety_percent = 0.0
stress_percent = 10.0

# Get suggestions based on predictions
suggestions = get_suggestions(depression_percent, anxiety_percent, stress_percent)

# Display suggestions
print("Suggestions based on predictions:")
for condition, suggestion in suggestions.items():
    print(f"{condition.capitalize()}: {suggestion}")

# Save the results to a file
save_results(depression_percent, anxiety_percent, stress_percent, suggestions)

# Visualize the results
plot_predictions(depression_percent, anxiety_percent, stress_percent)
