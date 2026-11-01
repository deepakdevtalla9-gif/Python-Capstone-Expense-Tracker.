import streamlit as st
import pandas as pd
from datetime import date
from expense_tracker.database import init_db, add_transaction, get_transactions, delete_transaction
from expense_tracker.analytics import summarize, category_totals
from expense_tracker.validators import validate_amount, validate_description
from expense_tracker.logger_config import get_logger

logger = get_logger()
st.set_page_config(page_title="Expense Tracker", page_icon="💰", layout="wide")
init_db()

st.title("💰 Personal Expense Tracker")
st.caption("Track income and expenses, understand your spending, and export your records.")

transactions = get_transactions()
summary = summarize(transactions)

c1, c2, c3 = st.columns(3)
c1.metric("Total Income", f"₹{summary['income']:,.2f}")
c2.metric("Total Expenses", f"₹{summary['expense']:,.2f}")
c3.metric("Available Balance", f"₹{summary['balance']:,.2f}")

st.divider()
tab_add, tab_history, tab_insights = st.tabs(["➕ Add Transaction", "📋 Transaction History", "📊 Insights"])

with tab_add:
    st.subheader("Add a new transaction")
    with st.form("transaction_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            transaction_type = st.selectbox("Transaction type", ["Expense", "Income"])
            amount = st.number_input("Amount (₹)", min_value=0.0, step=50.0, format="%.2f")
            transaction_date = st.date_input("Date", value=date.today())
        with col2:
            categories = (
                ["Food", "Travel", "Shopping", "Bills", "Education", "Health", "Other"]
                if transaction_type == "Expense"
                else ["Salary", "Freelance", "Gift", "Other Income"]
            )
            category = st.selectbox("Category", categories)
            description = st.text_input("Description", placeholder="e.g. Lunch, bus pass, monthly salary")
        submitted = st.form_submit_button("Save transaction", type="primary")
        if submitted:
            amount_error = validate_amount(amount)
            description_error = validate_description(description)
            if amount_error or description_error:
                st.error(amount_error or description_error)
            else:
                try:
                    add_transaction(transaction_type, amount, category, description.strip(), transaction_date.isoformat())
                    logger.info("Transaction added: %s, %.2f, %s", transaction_type, amount, category)
                    st.success("Transaction saved successfully.")
                    st.rerun()
                except Exception:
                    logger.exception("Could not save transaction")
                    st.error("Something went wrong while saving. Please try again.")

with tab_history:
    st.subheader("All transactions")
    if transactions.empty:
        st.info("No transactions yet. Add your first transaction from the Add Transaction tab.")
    else:
        filter_type = st.selectbox("Filter by type", ["All", "Income", "Expense"], key="history_filter")
        shown = transactions if filter_type == "All" else transactions[transactions["type"] == filter_type]
        st.dataframe(shown, use_container_width=True, hide_index=True)
        csv_data = shown.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download CSV report", csv_data, "expense_report.csv", "text/csv")
        transaction_ids = shown["id"].tolist()
        if transaction_ids:
            selected_id = st.selectbox(
                "Select a transaction ID to delete",
                transaction_ids,
                format_func=lambda x: f"Transaction #{x}"
            )
            if st.button("Delete selected transaction"):
                delete_transaction(int(selected_id))
                logger.info("Transaction deleted: %s", selected_id)
                st.success("Transaction deleted.")
                st.rerun()

with tab_insights:
    st.subheader("Spending insights")
    if transactions.empty or transactions[transactions["type"] == "Expense"].empty:
        st.info("Add some expenses to see your spending chart.")
    else:
        expense_data = category_totals(transactions)
        st.bar_chart(expense_data.set_index("category")["amount"])
        st.caption("Expenses grouped by category.")
        monthly = transactions.copy()
        monthly["month"] = pd.to_datetime(monthly["date"]).dt.to_period("M").astype(str)
        monthly = monthly[monthly["type"] == "Expense"].groupby("month", as_index=False)["amount"].sum()
        if not monthly.empty:
            st.subheader("Monthly expenses")
            st.line_chart(monthly.set_index("month")["amount"])

st.divider()
st.caption("Built with Python, Streamlit, SQLite and Pandas.")
