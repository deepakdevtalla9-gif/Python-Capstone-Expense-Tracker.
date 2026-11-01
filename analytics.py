def summarize(transactions):
    if transactions.empty:
        return {"income": 0.0, "expense": 0.0, "balance": 0.0}
    income = float(transactions.loc[transactions["type"] == "Income", "amount"].sum())
    expense = float(transactions.loc[transactions["type"] == "Expense", "amount"].sum())
    return {"income": income, "expense": expense, "balance": income - expense}

def category_totals(transactions):
    expenses = transactions[transactions["type"] == "Expense"]
    return expenses.groupby("category", as_index=False)["amount"].sum().sort_values("amount", ascending=False)
