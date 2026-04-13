# 🛡 PhishGuard — Phishing Email Detection System

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![Django](https://img.shields.io/badge/Django-5.2-green?style=flat-square&logo=django)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange?style=flat-square&logo=scikit-learn)
![License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square)

A full-stack web application that detects phishing emails using machine learning. Built with Django, it provides a complete email-like interface where every outgoing message is scanned in real time by a trained Logistic Regression pipeline. Senders of phishing emails are automatically blocked, and detailed sentiment analysis is displayed alongside the AI verdict when reading messages.

---

## ✨ Features

- 🤖 **Real-time AI scanning** — every sent email is classified as Safe or Phishing using a trained ML model
- 🚫 **Auto-block** — phishing senders are automatically added to the user's block list on inbox load
- 📧 **Full email workflow** — compose, inbox, outbox, drafts, read, delete
- 📊 **Sentiment analysis** — VADER NLP scores displayed alongside AI verdict on email read page
- 👤 **User management** — register, login, profile view/update, profile photo upload
- 🛡 **Admin panel** — manage users, review feedbacks, control block lists, view live stats
- 💬 **Feedback system** — users can submit feedback visible to admins
- 🎨 **Cyberpunk UI** — fully custom dark-themed responsive design across all 18 pages

---

## 🖥 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 5.2, Python 3.11 |
| Database | SQLite (dev) |
| ML Model | Logistic Regression — scikit-learn 0.23.2 |
| NLP | VADER Sentiment Analysis |
| Data | pandas, numpy |
| Frontend | HTML5, CSS3, Vanilla JS |
| Charts | Chart.js |
| Fonts | Orbitron, Rajdhani, Share Tech Mono (Google Fonts) |
| Auth | Django AbstractUser + session-based |

---

## 🗂 Project Structure

```
mailproject/
├── mailproject/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── mailapp/
│   ├── models.py          # All database models
│   ├── views.py           # All view functions
│   └── migrations/
├── templates/
│   ├── USER/              # User-facing pages
│   │   ├── userHome.html
│   │   ├── inbox.html
│   │   ├── compose.html
│   │   ├── readMail.html
│   │   ├── drafts.html
│   │   ├── readDrafts.html
│   │   ├── outBox.html
│   │   ├── profile.html
│   │   ├── updateProfile.html
│   │   ├── addFeedback.html
│   │   └── blockedUsers.html
│   ├── ADMIN/             # Admin panel pages
│   │   ├── adminHome.html
│   │   ├── viewUsers.html
│   │   ├── viewFeedbacks.html
│   │   └── blockedUsers.html
│   ├── index.html         # Landing page
│   ├── login.html
│   └── register.html
├── static/
│   ├── css/style.css
│   ├── js/
│   ├── images/
│   └── plugins/
├── Naive_model.pkl        # Trained ML pipeline (Logistic Regression)
├── phishing_site_urls.csv # URL dataset for URL-matching check
└── manage.py
```

---

## 🗃 Database Models

| Model | Purpose |
|---|---|
| `Login` | Extends AbstractUser — adds `userType` ('Admin'/'User') and `viewPass` |
| `UserRegistration` | Profile data: name, email, phone, DOB, gender, address, image |
| `Message` | Sent emails with `prediction_result` field ('0'=safe, '1'=phishing) |
| `Drafts` | Saved drafts — identical to Message, deleted on send |
| `Feedback` | User feedback submissions linked to UserRegistration |
| `BlockList` | Records blocking_user_id ↔ blocked_user_id pairs with status |

---

## 🤖 ML Pipeline

The model is a **scikit-learn Pipeline** combining:

1. `CountVectorizer` — tokenises URL text using `RegexpTokenizer(r'[A-Za-z]+')` with English stop words
2. `LogisticRegression` — binary classifier trained on labelled URLs

**Dataset:** [Kaggle — Phishing Site URLs](https://www.kaggle.com/datasets/taruntiwarihp/phishing-site-urls) — 549,346 labelled URLs (`bad` / `good`)

**Accuracy:** ~96% on test split (URL data)

> ⚠️ **Note:** Despite being named `Naive_model.pkl`, the saved model is **Logistic Regression**, not Naive Bayes. Naive Bayes was evaluated (~94%) but not saved.

> ⚠️ **Known limitation:** The model was trained on URL strings but is applied to email body text at runtime. This domain mismatch reduces real-world accuracy. Retraining on a phishing email dataset (SpamAssassin, CSDMC2010) is recommended for production use.

---

## 🚀 Installation

### Prerequisites
- Python 3.11+
- pip
- Git

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/phishguard.git
cd phishguard

# 2. Install dependencies
pip install django vaderSentiment pandas scikit-learn==0.23.2 pillow

# 3. Run migrations
python manage.py makemigrations
python manage.py migrate

# 4. Place required files in the project root
#    - Naive_model.pkl        (trained pipeline)
#    - phishing_site_urls.csv (URL dataset)

# 5. Start the development server
python manage.py runserver
```

Visit `http://127.0.0.1:8000`

> ⚠️ Pin `scikit-learn==0.23.2` to match the pickle version. Using a different version causes `InconsistentVersionWarning` and may break inference.

### Create an Admin User

```bash
python manage.py shell
>>> from mailapp.models import Login
>>> u = Login.objects.get(username='your@email.com')
>>> u.userType = 'Admin'
>>> u.save()
```

---

## 🔗 URL Routes

| URL | Description |
|---|---|
| `/` | Landing page |
| `/login` | Sign in |
| `/register` | Create account |
| `/userHome` | User dashboard |
| `/inbox` | Email inbox with AI badges |
| `/compose` | Compose + ML scan on send |
| `/readMail?id=N` | Read email + threat analysis |
| `/drafts` | Saved drafts |
| `/outBox` | Sent emails |
| `/viewProfile` | View profile |
| `/updateProfile` | Edit profile |
| `/addFeedback` | Submit feedback |
| `/blockedUsers` | Manage blocked senders |
| `/adminHome` | Admin dashboard |
| `/viewUsers` | Admin: manage users |
| `/viewFeedbacks` | Admin: review feedback |
| `/adminBlockedUsers` | Admin: manage block list |

---

## 🎨 UI Design

All pages use a consistent **cyberpunk dark theme**. Each section has its own accent colour:

| Section | Accent |
|---|---|
| General / Inbox | Cyan `#00d4ff` |
| Phishing / Danger | Red `#ff3860` |
| Safe / Feedback | Green `#39ff14` |
| Drafts / Warnings | Orange `#ff8c00` |
| Profile / Outbox | Purple `#a855f7` |

**Fonts:** Orbitron (headings) · Rajdhani (body) · Share Tech Mono (labels/code)

---

## ⚠️ Security Notes

- CSRF protection enabled on all forms
- All user views protected with session guard — redirects to `/login` if no session
- Passwords hashed via Django's PBKDF2 + SHA256
- `viewPass` stores plain text for admin display — **remove before production**
- Use PostgreSQL and set `DEBUG=False` for any public deployment

---

## 📁 Dependencies

```
django>=5.0
vaderSentiment
pandas
numpy
scikit-learn==0.23.2
Pillow
```

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgements

- [Kaggle — Phishing Site URLs Dataset](https://www.kaggle.com/datasets/taruntiwarihp/phishing-site-urls)
- [VADER Sentiment Analysis](https://github.com/cjhutto/vaderSentiment) — Hutto & Gilbert (2014)
- [scikit-learn](https://scikit-learn.org/) — Pedregosa et al., JMLR 2011
- [Chart.js](https://www.chartjs.org/) — MIT License
- [Google Fonts](https://fonts.google.com/) — Orbitron, Rajdhani, Share Tech Mono

📬 Support

If you have any questions or suggestions:

Open an issue in this repository
Contact via LinkedIn

👨‍💻 Maintainer

Akshay Suresh

🔗 LinkedIn: https://www.linkedin.com/in/akshay-suresh-a04202283|

💻 GitHub: https://github.com/Akshayy-y

⭐ Show Your Support

If you like this project, consider giving it a ⭐ on GitHub!
