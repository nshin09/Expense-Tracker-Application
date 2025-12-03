import plotly.graph_objs as go
import plotly.io as pio
from datetime import date
def monthlyTotals(expenses):
    today = date.today()
    year = today.year
    month = today.month

    months = []

    for _ in range(12):
        key = f"{year}-{month:02d}"
        months.append(key)

        month -= 1
        if month == 0:
            month = 12
            year -= 1
    months = months[::-1]

    totals = {m: 0 for m in months}

    # Add actual expense data
    for e in expenses:
        key = e.date.strftime("%Y-%m")
        if key in totals:
            totals[key] += e.amount

    # ordered lists
    x = months
    y = [totals[m] for m in months]

    return x, y

def create_expense_graph(expenses):
    months, values = monthlyTotals(expenses)

    fig = go.Figure(data=[
        go.Bar(x=months, y=values, hovertemplate="$%{y}<extra></extra>")
    ])

    fig.update_layout(
        title="Spending Over the Past Year (Per Month)",
        xaxis_title="Month (Year-Month)",
        yaxis_title="Total Spent ($)",
        height= 400,
        width = 800
    )
    fig.update_xaxes(
        tickmode="array",
        tickvals=months,
        ticktext=months
    )
    return pio.to_json(fig)

def highest_and_lowest_category(expenses):
    Food = 0.0
    Transport = 0.0
    Bills = 0.0
    Investment = 0.0
    Other = 0.0
    for expense in expenses:
        if expense.category == "Food":
            Food += expense.amount
        elif expense.category == "Bills":
            Transport += expense.amount
        elif expense.category == "Transport":
            Bills += expense.amount
        elif expense.category == "Investment":
            Investment += expense.amount
        else:
            Other += expense.amount
    highest = max(Food, Transport, Bills, Other, Investment)
    lowest = min(Food, Transport, Bills, Other, Investment)
    low_category = ""
    high_category = ""
    if lowest == Food:
        low_category = "Food"
    elif lowest == Bills:
        low_category = "Bills"
    elif lowest == Transport:
        low_category = "Transport" 
    elif lowest == Investment:
        low_category = "Investment"
    else:
        low_category = "Other"
    if highest == Food:
        high_category = "Food"
    elif highest == Bills:
        high_category = "Bills"
    elif highest == Transport:
        high_category = "Transport" 
    elif highest == Investment:
        high_category = "Investment"
    else:
        high_category = "Other"
    return (highest,high_category), (lowest,low_category)