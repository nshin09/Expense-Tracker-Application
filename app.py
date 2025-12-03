from flask import Flask, render_template, request,redirect
from waitress import serve
from flask_sqlalchemy import SQLAlchemy
from datetime import  date, datetime
from visualization import create_expense_graph, highest_and_lowest_category
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expense.db'
db = SQLAlchemy(app)


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(30))
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(20))
    date =  db.Column(db.Date, nullable=False, default = date.today)

with app.app_context():
    db.create_all()


@app.route('/', methods=["GET", "POST"])
def index():
    expense_date = None # Used to autofill the expense date to the present day. 
    if request.method == "POST":
        description = request.form['description']
        amount = float(request.form['amount'])
        category = request.form['category']
        expense_date = datetime.strptime(request.form['date'], "%Y-%m-%d").date()

        new_expense = Expense(description=description, amount=amount,
                              category=category, date=expense_date)
        db.session.add(new_expense)
        db.session.commit()
        return redirect("/")
    
    query = Expense.query 
    expenses = query.order_by(Expense.date.desc()).all()
    high, low = highest_and_lowest_category(expenses) # highest and lowest spendings are calculated with all expenses.
    grand_total = sum(e.amount for e in expenses) # grand total calculates all expenses. 

    selected_categories = request.args.getlist('filter_categories')  # list of selected categories from filter. 
    if selected_categories:
        query = query.filter(Expense.category.in_(selected_categories))

    expenses = query.order_by(Expense.date.desc()).all()
    graphJSON = create_expense_graph(expenses)
    total = sum(e.amount for e in expenses)

    if not expense_date:
        expense_date = date.today().strftime("%Y-%m-%d")
        
    return render_template("index.html",expenses = expenses, grand_total = grand_total, total = total, date = expense_date, selected_categories=selected_categories, graphJSON = graphJSON,
                           high = high[0], low = low[0], low_category = low[1], high_category = high[1] )

@app.route("/delete/<int:id>")
def delete(id):
    expense = Expense.query.get(id)
    db.session.delete(expense)
    db.session.commit()
    return redirect("/")
    
if __name__ == "__main__":
    serve(app, host = "0.0.0.0", port = 8000)

