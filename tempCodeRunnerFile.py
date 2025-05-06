
# # Prediction route
# @app.route('/predict', methods=['POST'])
# def predict():
#     # Collect form data
    
#     user_data = {
#         'feeling_today': request.form['feeling_today'],
#         'stress_level': request.form['stress_level'],
#         'sleep_quality': request.form['sleep_quality'],
#         'eating_healthy': request.form['eating_healthy'],
#         'exercise_frequency': request.form['exercise_frequency'],
#         'social_support': request.form['social_support'],
#          'feeling_today': request.form['feeling_today'],
#     'stress_level': request.form['stress_level'],
#     'sleep_quality': request.form['sleep_quality'],
#     'eating_healthy': request.form['eating_healthy'],
#     'exercise_frequency': request.form['exercise_frequency'],
#     'social_support': request.form['social_support'],
#     'routine_satisfaction': request.form['routine_satisfaction'],
#     'recent_happiness': request.form['recent_happiness'],
#     'relaxation_frequency': request.form['relaxation_frequency'],
#     'overwhelmed': request.form['overwhelmed'],
#     'social_connection': request.form['social_connection'],
#     'emotional_selfcare': request.form['emotional_selfcare'],
#     'motivation': request.form['motivation'],
#     'lifestyle_happiness': request.form['lifestyle_happiness'],
#     'goal_setting': request.form['goal_setting']


#         # Add any additional required fields here
#     }

#     # Create DataFrame from form input
#     input_df = pd.DataFrame([user_data])

#     # Apply label encoding to necessary columns
#     for col in input_df.columns:
#         if col in label_encoders:
#             input_df[col] = label_encoders[col].transform(input_df[col])

#     # Predict
#     predictions = model.predict(input_df)

#     # Format predictions and suggestions
#     result = interpret_results(predictions)

#     # Render results page
#     return render_template('results.html', result=result)

# # Interpret the model output
# def interpret_results(predictions):
#     depression_percent, anxiety_percent, stress_percent = predictions[0]
#     return {
#         'depression': depression_percent,
#         'anxiety': anxiety_percent,
#         'stress': stress_percent,
#         'suggestions': generate_suggestions(depression_percent, anxiety_percent, stress_percent)
#     }

# # Generate personalized suggestions
# def generate_suggestions(depression, anxiety, stress):
#     return {
#         'depression': "Consider seeing a counselor or practicing relaxation techniques." if depression > 50 else "Keep up with healthy habits, stay active.",
#         'anxiety': "Practice mindfulness or talk to a therapist." if anxiety > 50 else "Keep maintaining your healthy habits.",
#         'stress': "Consider reducing workload or practicing stress-relieving exercises." if stress > 50 else "Continue maintaining a stress-free routine."
#     }
