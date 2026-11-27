# Student Academic Risk Prediction System

## Project Description
The Student Academic Risk Prediction System is a Python-based application developed using Streamlit. It helps analyze student academic performance and identify students who may be academically at risk.

## Project Objectives
- Analyze student attendance and marks.
- Monitor academic performance.
- Identify students with high, medium and low academic risk.
- Provide an interactive dashboard.
- Allow users to register and log in securely.

## Technologies Used
- Python
- Streamlit
- Pandas
- Plotly
- SQLite3
- Bcrypt
- NumPy

## Main Features
1. User Signup and Login.
2. SQLite database integration.
3. Secure password hashing.
4. Interactive academic dashboard.
5. Student marks visualization.
6. Attendance analysis.
7. Academic risk distribution.
8. Student search and risk filtering.
9. Download student records as CSV.
10. Simulated academic risk prediction.

## Project Structure
```text
Student_Academic_Risk_System/
│
├── app.py
├── auth.py
├── requirements.txt
├── README.md
├── .gitignore
├── database/
│   └── auth.db
├── pages/
└── venv/
```

Note: The database and virtual environment are excluded from GitHub.

## Installation Instructions

### 1. Clone the repository
```bash
git clone YOUR_GITHUB_REPOSITORY_LINK
```

### 2. Open the project folder
```bash
cd Student_Academic_Risk_System
```

### 3. Create virtual environment
```bash
python -m venv venv
```

### 4. Activate virtual environment (Windows)
```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install dependencies
```bash
pip install -r requirements.txt
```

### 6. Run the application
```bash
streamlit run app.py
```

## Dataset
Sample dummy student records are currently used for dashboard development. A public Student Performance dataset will be selected for the future machine learning stage.

## Prediction Method
The current application uses simulated rule-based predictions. Actual machine learning model training and evaluation will be implemented in the final project.

## Future Improvements
- Real dataset integration.
- Data preprocessing.
- Exploratory Data Analysis (EDA).
- Machine learning classification.
- Model evaluation.
- Improved prediction accuracy.

## Author
Benish Sehar


