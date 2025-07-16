# Smart Health Disease Prediction

This is a machine learning-based website built with *Python Flask* that predicts possible diseases based on user input symptoms.

## 📂 Project Files

- app.py — Flask server backend
- disease_prediction.py — Core prediction logic
- model.pkl, disease_prediction_model.pkl — Trained ML models
- symptoms.pkl — Pickled symptoms data
- doctors_data.json — Doctor information mapped to diseases
- symptoms_disease_dataset.csv — Dataset used for training
- index.html, login.html, results.html, symptoms.html — Frontend web pages
- style.css — CSS styling
- script.js — JavaScript for frontend
- robot-doctor.png — Image used in the UI

  ## 🛠️ Technologies Used

- *Frontend:* HTML, CSS  
- *Backend:* Python, Flask framework  
- *Machine Learning:*  
  - *Algorithm:* Random Forest Classifier  
  - *Libraries:* pandas, scikit-learn, joblib  
- *Storage:*  
  - disease_prediction_model.pkl (trained ML model)  
  - symptoms.pkl (symptom list)  
  - doctors_data.json (doctor details)

---

## 📊 Datasets Used

- *Source:* symptoms_disease_dataset.csv
- *Features:* Symptom columns (symptom_1, symptom_2, …)
- *Target:* Disease name
- *Processing:*  
  - Converted symptoms into binary features  
  - Used for training and testing the model
- *Split:* 80% training, 20% testing

---

## 🤖 Machine Learning Algorithm

- *Algorithm Used:* Random Forest Classifier (for disease prediction)

---

## ⚙️ How to Run

1. *Clone or download* this repository.
2. Open the project folder in *Visual Studio Code*.
3. Make sure you have *Python* installed.  
   Install required Python packages if not already installed:
   ```bash
   pip install flask pandas scikit-learn


## 👤 Author

M Siddartha Yadav
