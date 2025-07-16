from flask import Flask, render_template, request, redirect, url_for, session
import joblib
import json
import numpy as np

DISEASE_DOCTOR_MAP = {
    "Covid-19": "General Physician",
    "Flu": "General Physician",
    "Migraine": "Neurologist",
    "Hypothyroidism": "Endocrinologist",
    "Diabetes": "Endocrinologist",
    "Heart Disease": "Cardiologist"
}

app = Flask(__name__)
app.secret_key = 'your-secret-key'
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Load the disease prediction model and symptoms
try:
    model = joblib.load("./disease_prediction_model.pkl")  # Disease prediction model
    ALL_SYMPTOMS = joblib.load('symptoms.pkl')  # List of symptoms used in training
except Exception as e:
    print(f"Error loading model: {e}")
    from sklearn.dummy import DummyClassifier
    model = DummyClassifier(strategy="constant", constant="Common Cold")
    model.fit([[0]*3], ["Common Cold"])
    ALL_SYMPTOMS = ["Fever", "Cough", "Headache"]  # Dummy symptoms if model doesn't load

# Load doctor data from doctor_data.json
try:
    with open('doctors_data.json', 'r') as f:
        DOCTORS_DATA = json.load(f)  # Read doctors' data from the JSON file
except FileNotFoundError:
    DOCTORS_DATA = []
    print("Warning: Could not load doctor data")


def get_recommended_doctors(predicted_disease):
    recommended = []

    specialization = DISEASE_DOCTOR_MAP.get(predicted_disease)

    if specialization and specialization in DOCTORS_DATA:
        for doctor in DOCTORS_DATA[specialization]:
            recommended.append({
                "name": doctor.get('name', 'Unknown'),
                "specialization": specialization,  # Use the outer variable
                "phone": doctor.get('phone', 'N/A'),
                "email": doctor.get('email', 'N/A'),
                "hospital": doctor.get('hospital', 'N/A'),
                "matched_disease": predicted_disease
            })

    return recommended



# Initialize session data
def initialize_session():
    if 'user' not in session:
        session['user'] = {'name': '', 'age': '', 'gender': ''}
    if 'selected_symptoms' not in session:
        session['selected_symptoms'] = []
    if 'results' not in session:
        session['results'] = {'disease': '', 'confidence': 0, 'doctors': []}

@app.route('/')
def home():
    initialize_session()
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    initialize_session()
    if request.method == 'POST':
        session['user'] = {
            'name': request.form.get('name', '').strip(),
            'age': request.form.get('age', '').strip(),
            'gender': request.form.get('gender', '').strip()
        }
        return redirect(url_for('symptoms'))
    return render_template('login.html', user=session['user'])

@app.route('/symptoms', methods=['GET', 'POST'])
def symptoms():
    initialize_session()
    if not session['user'].get('name'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        selected_symptoms = request.form.getlist('symptoms')
        session['selected_symptoms'] = selected_symptoms

        # Prepare input for prediction
        input_vector = [1 if symptom in selected_symptoms else 0 for symptom in ALL_SYMPTOMS]

        # Predict disease
        predicted_disease = model.predict([input_vector])[0]
        
        # Confidence Calculation
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba([input_vector])[0]
            confidence = round(100 * max(proba), 2)  # Get the maximum probability for confidence
        else:
            confidence = 100  # If no probability method is available, set confidence to 100%

        # Get recommended doctors based on predicted disease
        recommended_doctors = get_recommended_doctors(predicted_disease)
        
        # Store results in session
        session['results'] = {
            'disease': predicted_disease,
            'confidence': confidence,
            'doctors': recommended_doctors
        }
        
        return redirect(url_for('results'))

    return render_template('symptoms.html', symptoms=ALL_SYMPTOMS, user=session['user'])


@app.route('/results')
def results():
    initialize_session()
    if not session['selected_symptoms']:
        return redirect(url_for('symptoms'))
    
    return render_template('results.html',
                           user=session['user'],
                           symptoms=session['selected_symptoms'],
                           results=session['results'])

@app.route('/clear')
def clear_session():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
