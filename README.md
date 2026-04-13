🛡️ PhishGuard — Phishing Email Detection System

📌 What This Project Does

PhishGuard is a full-stack cybersecurity web application that detects phishing emails using machine learning and natural language processing.

It simulates a real-world email system where messages are analyzed in real time and classified as safe or phishing, helping users identify malicious content and understand phishing behavior.

Why This Project Is Useful

Phishing attacks are one of the most common cybersecurity threats. This project demonstrates how to:

Detect phishing attempts using machine learning
Analyze email content for suspicious patterns
Apply defensive security mechanisms like user blocking
Combine backend systems, ML, and UI for real-world security applications

Key Features
Real-time phishing detection (ML model)
Sentiment analysis using VADER NLP
Full email workflow (compose, inbox, drafts, outbox)
User authentication & session management
Automatic sender blocking for phishing emails
Admin dashboard for monitoring users and threats

Tech Stack
Layer	Technology
Backend	Django (Python)
Machine Learning	Logistic Regression (scikit-learn)
NLP	VADER Sentiment Analysis
Database	SQLite
Frontend	HTML, CSS, JavaScript
Libraries	pandas, numpy

Getting Started
Prerequisites
Python 3.11+
Git
pip

🔧 Installation
git clone https://github.com/yourusername/phishguard.git
cd phishguard
pip install -r requirements.txt
🗄️ Database Setup
python manage.py makemigrations
python manage.py migrate

▶️ Run the Application
python manage.py runserver

👉 Open in browser:

http://127.0.0.1:8000
👤 Usage Example
Register a new user
Login to the system
Compose an email
System analyzes content → flags phishing/safe
View inbox with detection results

🧠 How It Works
Email content is processed using a trained ML pipeline
Text is tokenized and vectorized
Logistic Regression model classifies content
VADER NLP provides sentiment analysis
Results are displayed in UI with visual indicators


<img width="1351" height="683" alt="Screenshot 2026-04-07 113807" src="https://github.com/user-attachments/assets/b329126b-cd44-42f5-92c6-d072d2af240d" />
<img width="2" height="1" alt="Screenshot 2026-04-07 113750" src="https://github.com/user-attachments/assets/8c192a09-5d4c-49fa-afd0-c6054a723519" />
<img width="1366" height="768" alt="Screenshot 2026-04-07 113726" src="https://github.com/user-attachments/assets/00ee5d4f-90ee-4b65-8939-442eebee6526" />
<img width="1352" height="682" alt="Screenshot 2026-04-07 113617" src="https://github.com/user-attachments/assets/504d9463-8116-4739-803e-a082d072e795" />
<img width="1363" height="680" alt="Screenshot 2026-04-07 113446" src="https://github.com/user-attachments/assets/5d095b05-0bd3-4b04-9fce-ad3284bc2de9" />
<img width="1365" height="679" alt="Screenshot 2026-04-07 113222" src="https://github.com/user-attachments/assets/7ee21d8f-07ee-4e53-9a37-1d6ab3edd6ae" />
<img width="1344" height="665" alt="Screenshot 2026-04-07 113130" src="https://github.com/user-attachments/assets/028b8cd4-e546-46bc-8377-b9bf96608e79" />
<img width="1350" height="686" alt="Screenshot 2026-04-07 112956" src="https://github.com/user-attachments/assets/5575536f-7d0f-40f4-b317-00c8062748d0" />

⚠️ Limitations
Model trained on URL dataset (not email dataset)
SQLite used (not production-ready)
No login rate limiting (brute-force risk)
Plain-text password field present (should be removed)
🚀 Future Improvements
Train model on phishing email datasets
Add email verification system
Implement rate limiting & 2FA
Upgrade database to PostgreSQL
Integrate real email APIs (Gmail/Outlook)
🤝 Contributing

Contributions are welcome!

Fork the repository
Create a new branch
Make changes
Submit a pull request
📬 Support

If you have any questions or suggestions:

Open an issue in this repository
Contact via LinkedIn
👨‍💻 Maintainer

Akshay Suresh

🔗 LinkedIn: https://www.linkedin.com/in/akshay-suresh-a04202283
💻 GitHub: https://github.com/Akshayy-y
⭐ Show Your Support

If you like this project, consider giving it a ⭐ on GitHub!
