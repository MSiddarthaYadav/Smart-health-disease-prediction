import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

def train_model():
    # Load dataset
    df = pd.read_csv('symptoms_disease_dataset.csv')

    # Get all unique symptoms
    symptoms = set()
    for col in df.columns:
        if col.startswith('symptom_'):
            symptoms.update(df[col].unique())

    symptoms = [s for s in symptoms if pd.notna(s)]
    symptoms.sort()

    # Create binary features for each symptom
    for symptom in symptoms:
        df[symptom] = df.apply(lambda row: 1 if symptom in row.values else 0, axis=1)

    # Prepare features and target
    X = df[symptoms]
    y = df['disease']

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    # Evaluate model
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    print(f"Model Accuracy: {accuracy:.2f}")
    print("Classification Report:\n", report)

    # Save model and symptoms list
    joblib.dump(clf, 'disease_prediction_model.pkl')
    joblib.dump(symptoms, 'symptoms.pkl')
    print("Model saved as 'disease_prediction_model.pkl'")
    print("Symptoms list saved as 'symptoms.pkl'")

train_model()
