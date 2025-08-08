
<!-- FinTrack Header -->

<p align="center">
  <img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" alt="Banner" />
</p>

<h1 align="center">💸 FinTrack</h1>
<p align="center"><b>Personal finance dashboard to track income, expenses, and visualize spending patterns.</b></p>
<p align="center">Built with Flask, SQLite, and TailwindCSS</p>


<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif">

## 📊 Features

- 🔐 Secure login-free local storage (via SQLite)
- 💰 Add & categorize income or expenses
- 📅 Filter & sort transactions by category or amount
- 📈 Interactive analytics: savings trends, income vs expenses, top expenses
- 🎨 Custom chart colors per category
- 🗂️ Manage income & expense categories easily

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif">

## ⚙️ Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=flat-square&logo=tailwindcss&logoColor=white)
![HTML](https://img.shields.io/badge/HTML-E34F26?style=flat-square&logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS-1572B6?style=flat-square&logo=css3&logoColor=white)

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif">

## 🖼️ Screenshots

| Summary | Transactions |
|--------|--------------|
| <img src="images/1.png" width="400"/> | <img src="images/2.png" width="400"/> |

| Categories | Analytics |
|-----------|-----------|
| <img src="images/3.png" width="400"/> | <img src="images/4.png" width="400"/> |

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif">

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/notgautham/FinTrack.git
cd FinTrack
````

### 2. (Optional) Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install Flask Flask_SQLAlchemy
```

### 4. Run the Application

```bash
python app.py
```

### 5. Visit [http://localhost:5000](http://localhost:5000) in your browser.



### 🛑 The app auto-generates a local `finance.db` SQLite file on first run. No setup needed.

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif">

## 📁 Project Structure

```
FinTrack/
│
├── app.py                # Main Flask app with all routes
├── finance.db            # Auto-generated SQLite database
├── /templates            # HTML templates (Jinja2)
├── /static               # Tailwind CSS & JS files
├── /screenshots          # UI screenshots (for README)
└── requirements.txt      # Python dependencies (optional)
```

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif">
