import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)

# Configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, "finance.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Create necessary folders
folders = ['static', 'templates']
files = {
    'templates/base.html': """<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>FinTrack</title>
    <style>
        body { background-color: #121212; color: white; font-family: Arial, sans-serif; }
    </style>
</head>
<body>
    <h1>Welcome to FinTrack</h1>
</body>
</html>""",
    'app.py': """from flask import Flask, render_template
from models import db

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)""",
    'models.py': """from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(10), nullable=False)  # 'income' or 'expense'
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    note = db.Column(db.String, nullable=True)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    type = db.Column(db.String(10), nullable=False)  # 'income' or 'expense'
    chart_color = db.Column(db.String, nullable=True)"""
}

# Create folders if they don't exist
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Create files with default content
for file, content in files.items():
    with open(file, 'w') as f:
        f.write(content)

print("FinTrack setup completed. Run `python app.py` to start the app.")