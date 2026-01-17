# 🏏 IPL Win Probability Predictor

An end-to-end Machine Learning project that predicts the **win probability of the chasing team (2nd innings)** in an IPL match based on the current match situation.

The app takes live match inputs such as **score, overs, wickets, target, teams, and city**, and returns the **winning probability (%)** using a trained ML model.

---

## 🚀 Live Demo
🔗 **Streamlit App:** *(https://ipl-match-win-probability-predictor.streamlit.app)*

---

## 📌 Features
✅ Predicts win probability in real-time during 2nd innings  
✅ IPL-style **win probability bar UI**  
✅ Shows **match situation summary** (runs left, balls left, CRR, RRR)  
✅ Clean and responsive Streamlit interface  
✅ Uses a trained ML pipeline (`pipe.pkl`) for fast predictions

---

## 🧠 How It Works (ML Workflow)

### 1️⃣ Data Source
The model is trained using IPL ball-by-ball and match-level datasets:
- `matches.csv`
- `deliveries.csv`

### 2️⃣ Feature Engineering (Match Situation)
From ball-by-ball data, the following features are generated:

- **runs_left** = target − current_score  
- **balls_left** = 120 − balls_bowled  
- **wickets_left** = 10 − wickets_out  
- **crr (Current Run Rate)** = score / overs  
- **rrr (Required Run Rate)** = (runs_left × 6) / balls_left  

### 3️⃣ Model Training
- Categorical features (teams, city) are encoded using **OneHotEncoder**
- Model used: **Logistic Regression**
- Training is done using a **Scikit-learn Pipeline**

---

## 🛠️ Tech Stack
- **Python**
- **Pandas, NumPy**
- **Scikit-learn**
- **Streamlit**
- **Pickle** (for saving trained pipeline)

---

## 📂 Project Structure
```bash
ipl-win-probability-predictor/
│── app/
│   ├── app.py
│   ├── pipe.pkl
│   ├── BG.jpg
│   ├── requirements.txt
│── README.md
```

