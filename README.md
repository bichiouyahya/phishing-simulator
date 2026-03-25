# 🛡️ Phishing Simulation Platform

A cybersecurity project that simulates phishing campaigns to analyze user behavior and demonstrate how real-world phishing attacks work.

---

## 🚀 Features

- 📧 Send phishing simulation emails using SMTP
- 🔗 Unique token-based tracking links
- 👆 Click tracking (records IP address & user-agent)
- 🔐 Credential capture system (educational use)
- 📊 Interactive dashboard with statistics and charts

---

## 🧠 How It Works

1. A phishing email is generated with a unique tracking link  
2. The user clicks the link → event is logged  
3. The user is redirected to a fake login page  
4. Submitted credentials are captured and stored  
5. The dashboard displays campaign results and analytics  

---

## 🛠️ Tech Stack

- **Backend:** FastAPI (Python)
- **Database:** SQLite + SQLAlchemy
- **Frontend:** HTML, CSS, Jinja2
- **Visualization:** Chart.js
- **Email:** SMTP (Gmail)

---

## 📊 Dashboard Preview

<img width="974" height="930" alt="1774462293" src="https://github.com/user-attachments/assets/34d8a4bc-d957-49c7-8587-8ad6c214b0dc" />

---

## ⚙️ Setup & Installation

```bash
git clone https://github.com/bichiouyahya/phishing-simulator.git
cd phishing-simulator
pip install -r requirements.txt```

Create a .env file:
```bash
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password```

Run the Application
```bash
uvicorn main:app --reload```

Testing Flow
Generate test data:
/setup-test
Change reciever email (main.py):
target = Target(
    email="example@test.com",
    name="Test User"
)
Send phishing email:
/send-test
Click the link from your email
Submit credentials
View results in dashboard:
/dashboard


⚠️ Disclaimer

This project is intended for educational purposes only.

Do NOT use this system against real users without explicit consent.

📌 Future Improvements
Admin authentication system
GeoIP tracking (victim location)
Export results (CSV)
Improved UI/UX
