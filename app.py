


# from flask import Flask, render_template, request, jsonify
# import pickle
# import os
# import pandas as pd
# from llama_engine import get_response  # Using your GGUF model

# app = Flask(__name__)

# # Load the trained model and label encoders
# model = pickle.load(open('mental_health_model.pkl', 'rb'))
# label_encoders = pickle.load(open('label_encoders.pkl', 'rb'))

# # Home route
# @app.route('/')
# def home():
#     return render_template('index.html')

# # Chat interface route
# @app.route('/chat')
# def chat():
#     return render_template('chat.html')

# @app.route('/therapist')
# def therapist():
#     return render_template('therapist.html')

# # Results page
# @app.route('/result')
# def result():
#     return render_template("results.html")

# # Safe transform to handle unseen labels
# def safe_transform(le, series):
#     return series.map(lambda val: le.transform([val])[0] if val in le.classes_ else -1)

# # Prediction route
# @app.route('/predict', methods=['POST'])
# def predict():
#     user_data = request.get_json()
#     input_df = pd.DataFrame([user_data])

#     # Apply label encoding
#     for col in input_df.columns:
#         if col in label_encoders:
#             input_df[col] = safe_transform(label_encoders[col], input_df[col])

#     predictions = model.predict(input_df)
#     result = interpret_results(predictions)
#     return jsonify(result)

# # Interpret model output
# def interpret_results(predictions):
#     depression_percent, anxiety_percent, stress_percent = predictions[0]
#     return {
#         "depression": float(depression_percent),
#         "anxiety": float(anxiety_percent),
#         "stress": float(stress_percent),
#         "suggestions": generate_suggestions(depression_percent, anxiety_percent, stress_percent)
#     }

# # Suggestion generator
# def generate_suggestions(depression, anxiety, stress):
#     return {
#         'depression': "Consider seeing a counselor or practicing relaxation techniques." if depression > 50 else "Keep up with healthy habits and stay active.",
#         'anxiety': "Practice mindfulness or talk to a therapist." if anxiety > 50 else "Keep maintaining your healthy habits.",
#         'stress': "Consider reducing workload or practicing stress-relieving exercises." if stress > 50 else "Continue maintaining a stress-free routine."
#     }

# # Chatbot response route using the GGUF model
# @app.route('/get_response', methods=['POST'])
# def chatbot_response():
#     user_input = request.json.get('user_input')
#     bot_response = get_response(user_input)  # Uses llama_engine.py
#     return jsonify({'response': bot_response})

# # Run the app with Gunicorn in production, no need for debug=True
# if __name__ == '__main__':
#     app.run()





from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
from llama_engine import get_response

app = Flask(__name__)

# Load ML model and encoders
model = pickle.load(open('mental_health_model.pkl', 'rb'))
label_encoders = pickle.load(open('label_encoders.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/therapist')
def therapist():
    return render_template('therapist.html')

@app.route('/result')
def result():
    return render_template("results.html")

# Safe label encoding
def safe_transform(le, series):
    return series.map(lambda val: le.transform([val])[0] if val in le.classes_ else -1)

@app.route('/predict', methods=['POST'])
def predict():
    user_data = request.get_json()
    input_df = pd.DataFrame([user_data])

    for col in input_df.columns:
        if col in label_encoders:
            input_df[col] = safe_transform(label_encoders[col], input_df[col])

    predictions = model.predict(input_df)
    result = interpret_results(predictions)
    return jsonify(result)

def interpret_results(predictions):
    depression_percent, anxiety_percent, stress_percent = predictions[0]
    return {
        "depression": float(depression_percent),
        "anxiety": float(anxiety_percent),
        "stress": float(stress_percent),
        "suggestions": generate_suggestions(depression_percent, anxiety_percent, stress_percent)
    }

def generate_suggestions(depression, anxiety, stress):
    return {
        'depression': "Consider seeing a counselor or practicing relaxation techniques." if depression > 50 else "Keep up with healthy habits and stay active.",
        'anxiety': "Practice mindfulness or talk to a therapist." if anxiety > 50 else "Keep maintaining your healthy habits.",
        'stress': "Consider reducing workload or practicing stress-relieving exercises." if stress > 50 else "Continue maintaining a stress-free routine."
    }

@app.route('/get_response', methods=['POST'])
def chatbot_response():
    user_input = request.json.get('user_input')
    bot_response = get_response(user_input)
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(debug=True)
