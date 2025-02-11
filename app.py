import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import jsonify
import calendar

app = Flask(__name__)

# Ensure the database file is created
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "finance.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)


# Define Models
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    type = db.Column(db.String(10), nullable=False)  # "income" or "expense"
    chart_color = db.Column(db.String(10), nullable=True)


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(10), nullable=False)  # "income" or "expense"
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    note = db.Column(db.String(200), nullable=True)

    # Add relationships
    category = db.relationship('Category', backref=db.backref('transactions', lazy=True))


# Create database and tables if they don't exist
with app.app_context():
    if not os.path.exists(DATABASE_PATH):
        db.create_all()
        print("Database created successfully!")


# Home Page (Redirect to Summary)
@app.route('/')
def index():
    return redirect(url_for('summary'))


# Summary Page
@app.route('/summary')
def summary():
    total_income = db.session.query(db.func.sum(Transaction.amount)).filter_by(type="income").scalar() or 0
    total_expense = db.session.query(db.func.sum(Transaction.amount)).filter_by(type="expense").scalar() or 0

    income_summary = db.session.query(Category.name, db.func.sum(Transaction.amount), Category.chart_color) \
        .join(Transaction).filter(Transaction.type == "income") \
        .group_by(Category.name, Category.chart_color).all()

    expense_summary = db.session.query(Category.name, db.func.sum(Transaction.amount), Category.chart_color) \
        .join(Transaction).filter(Transaction.type == "expense") \
        .group_by(Category.name, Category.chart_color).all()

    categories = Category.query.all()

    return render_template(
        'index.html',
        total_income=total_income,
        total_expense=total_expense,
        income_summary=income_summary,
        expense_summary=expense_summary,
        categories=categories
    )

@app.route('/analytics-data')
def analytics_data():
    import calendar

    # Expense breakdown by category
    expense_breakdown = db.session.query(
        Category.name,
        db.func.sum(Transaction.amount).label('total')
    ).join(Transaction).filter(Transaction.type == 'expense').group_by(Category.name).all()
    expense_breakdown = [{'category': c, 'total': t} for c, t in expense_breakdown]

    # Income vs Expense Over Time
    income_vs_expense = db.session.query(
        db.func.strftime('%m', Transaction.date).label('month'),
        db.func.strftime('%Y', Transaction.date).label('year'),
        db.func.sum(db.case((Transaction.type == 'income', Transaction.amount), else_=0)).label('income'),
        db.func.sum(db.case((Transaction.type == 'expense', Transaction.amount), else_=0)).label('expense')
    ).group_by('year', 'month').all()

    # Convert month numbers to full names
    income_vs_expense = [{'month': f"{calendar.month_name[int(m)]} {y}", 'income': i, 'expense': e} for m, y, i, e in income_vs_expense]

    # Monthly savings trend
    savings = [{'month': entry['month'], 'savings': entry['income'] - entry['expense']} for entry in income_vs_expense]

    # Largest expenses
    largest_expenses = db.session.query(
        Transaction.note,
        Transaction.amount
    ).filter(Transaction.type == 'expense').order_by(Transaction.amount.desc()).limit(5).all()
    largest_expenses = [{'note': n, 'amount': a} for n, a in largest_expenses]

    return jsonify({
        'expense_breakdown': expense_breakdown,
        'income_vs_expense': income_vs_expense,
        'savings': savings,
        'largest_expenses': largest_expenses,
    })


# Transactions Page
@app.route('/transactions', methods=['GET'])
def transactions():
    # Fetch query parameters for sorting and filtering
    sort_by = request.args.get('sort_by', 'date')  # Default to sorting by date
    selected_category = request.args.get('category', 'all')  # Default to show all categories

    # Base query
    query = Transaction.query

    # Apply category filter if a specific category is selected
    if selected_category != 'all':
        query = query.filter(Transaction.category_id == int(selected_category))

    # Apply sorting
    if sort_by == 'amount':
        query = query.order_by(Transaction.amount.desc())
    elif sort_by == 'category':
        query = query.join(Category).order_by(Category.name)
    else:  # Default to sorting by date
        query = query.order_by(Transaction.date.desc())

    # Fetch filtered and sorted transactions
    transactions = query.all()

    # Fetch all categories for filtering dropdown
    categories = Category.query.all()

    return render_template('transactions.html', transactions=transactions, categories=categories)



@app.route('/edit_transaction/<int:id>', methods=['GET', 'POST'])
def edit_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    categories = Category.query.all()

    if request.method == 'POST':
        # Update transaction details from the form
        transaction.date = datetime.strptime(request.form.get('date'), '%Y-%m-%d')
        transaction.amount = float(request.form.get('amount'))
        transaction.type = request.form.get('type')
        transaction.category_id = int(request.form.get('category'))
        transaction.note = request.form.get('note')

        db.session.commit()
        flash("Transaction updated successfully!", "success")
        return redirect(url_for('transactions'))

    return render_template('edit_transaction.html', transaction=transaction, categories=categories)



# Add Transaction
@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    date = request.form.get('date')
    amount = float(request.form.get('amount'))
    trans_type = request.form.get('type')
    category_id = int(request.form.get('category'))
    note = request.form.get('note')

    new_transaction = Transaction(
        date=datetime.strptime(date, '%Y-%m-%d'), amount=amount, type=trans_type, category_id=category_id, note=note
    )
    db.session.add(new_transaction)
    db.session.commit()

    flash("Transaction added successfully!", "success")
    return redirect(url_for('transactions'))


# Delete Transaction
@app.route('/delete_transaction/<int:id>')
def delete_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    db.session.delete(transaction)
    db.session.commit()

    flash("Transaction deleted!", "danger")
    return redirect(url_for('transactions'))


# Categories Page
@app.route('/categories')
def categories():
    income_categories = Category.query.filter_by(type="income").all()
    expense_categories = Category.query.filter_by(type="expense").all()
    return render_template('categories.html', income_categories=income_categories,
                           expense_categories=expense_categories)


# Add Category (Fixed)
@app.route('/add_category', methods=['POST'])
def add_category():
    name = request.form.get('category-name')  # Match this with your form field
    cat_type = request.form.get('category-type')
    chart_color = request.form.get('chart-color')

    if not name or not cat_type:
        flash("Category name and type are required!", "warning")
        return redirect(url_for('categories'))

    if Category.query.filter_by(name=name).first():
        flash("Category already exists!", "warning")
    else:
        new_category = Category(name=name, type=cat_type, chart_color=chart_color)
        db.session.add(new_category)
        db.session.commit()
        flash("Category added successfully!", "success")

    return redirect(url_for('categories'))

#edit category
@app.route('/edit_category/<int:id>', methods=['GET', 'POST'])
def edit_category(id):
    category = Category.query.get_or_404(id)

    if request.method == 'POST':
        category.name = request.form.get('category-name')
        category.type = request.form.get('category-type')
        category.chart_color = request.form.get('chart-color')

        db.session.commit()
        flash("Category updated successfully!", "success")
        return redirect(url_for('categories'))

    return render_template('edit_category.html', category=category)



# Delete Category
@app.route('/delete_category/<int:id>')
def delete_category(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()

    flash("Category deleted!", "danger")
    return redirect(url_for('categories'))


# Analytics Page
@app.route('/analytics')
def analytics():
    return render_template('analytics.html')


if __name__ == '__main__':
    app.run(debug=True)
