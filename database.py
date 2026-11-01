import sqlite3
from pathlib import Path
import pandas as pd

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "expenses.db"

def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection

def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL CHECK(type IN ('Income', 'Expense')),
                amount REAL NOT NULL CHECK(amount > 0),
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                date TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

def add_transaction(transaction_type, amount, category, description, transaction_date):
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO transactions (type, amount, category, description, date)
               VALUES (?, ?, ?, ?, ?)""",
            (transaction_type, float(amount), category, description, transaction_date)
        )
        conn.commit()

def get_transactions():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, type, amount, category, description, date FROM transactions ORDER BY date DESC, id DESC"
        ).fetchall()
    return pd.DataFrame([dict(row) for row in rows],
                        columns=["id", "type", "amount", "category", "description", "date"])

def delete_transaction(transaction_id):
    with get_connection() as conn:
        conn.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
        conn.commit()
