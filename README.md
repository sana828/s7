🩺 Project Overview

Epilepsy is one of the most common neurological disorders, characterized by recurrent seizures caused by abnormal brain activity.
Manual EEG interpretation by experts is time-consuming and error-prone.
This project automates the process by using Machine Learning models to detect seizure patterns from EEG data.

The web application allows:

🧠 Patients to upload EEG signal files

⚙️ ML model to predict seizure type

👩‍⚕️ Doctors to review results and assist patients

💬 Both to communicate and share feedback

🎯 Objectives

Automate seizure detection from EEG signals

Classify EEG recordings into seizure severity levels

Provide a simple and interactive web interface for users

Bridge patients and doctors via an appointment system

Maintain medical feedback and history

🧩 System Architecture

1️⃣ Data Input:
Patient uploads EEG signal data (.csv format).

2️⃣ Preprocessing:
EEG data is processed using Pandas for cleaning and formatting.

3️⃣ Model Prediction:
The trained Random Forest model (rf.pkl) classifies the signal into one of five categories:

1️⃣ Normal

2️⃣ Mild

3️⃣ Moderate

4️⃣ Severe

5️⃣ Critical

4️⃣ Database Management:
Predicted results and user info are stored in SQLite.

5️⃣ Doctor Recommendation:
Based on predicted severity, the system lists doctors in the corresponding specialization.

6️⃣ Feedback System:
Patients can rate and review their experiences for future improvements.

⚙️ System Modules
👨‍⚕️ Doctor Module

Register & login

View patients assigned based on prediction level

Manage consultation timings

View and respond to feedback

👩‍⚕️ Patient Module

Register & login

Upload EEG CSV file for prediction

View assigned doctor(s)

Confirm appointments via OTP

Submit feedback

🧑‍💼 Admin Module

View all registered doctors and patients

Oversee system operations

💻 Technologies Used
Category	Tools & Libraries
Frontend	HTML5, CSS3
Backend	Flask (Python)
Database	SQLite3
Machine Learning	Scikit-learn, Pandas, Pickle
Security	Flask Sessions, Secrets
Miscellaneous	Random (for OTP)







📊 Example Workflow

1️⃣ Patient registers and logs in
2️⃣ Uploads EEG data (test.csv)
3️⃣ System predicts seizure category
4️⃣ Lists available doctors
5️⃣ Patient confirms appointment via OTP
6️⃣ Feedback submitted post-consultation
