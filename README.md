# Personal Expense Tracker

A portfolio-ready Python application for recording income and expenses, reviewing balances, viewing spending insights, and exporting transaction data.

## Features
- Add income and expense transactions
- Categorize transactions
- Store records in a local SQLite database
- View total income, expenses, and available balance
- Filter and delete transactions
- Export transaction history as CSV
- View category-wise and monthly spending charts
- Input validation, exception handling, and application logging

## Tech stack
- Python
- Streamlit
- SQLite
- Pandas

## Project structure
```text
python_capstone_expense_tracker/
├── app.py
├── expense_tracker/
│   ├── __init__.py
│   ├── analytics.py
│   ├── database.py
│   ├── logger_config.py
│   └── validators.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Setup instructions

### 1. Install Python
Install Python 3.10 or newer and verify:
```bash
python --version
```

### 2. Open the project folder
Open this folder in VS Code, then open the terminal.

### 3. Create and activate a virtual environment (recommended)
Windows:
```powershell
py -m venv .venv
.venv\\Scripts\\Activate.ps1
```
If PowerShell blocks activation, run:
```powershell
.venv\\Scripts\\activate.bat
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the app
```bash
streamlit run app.py
```
The app will open in your browser. If it does not, open the local URL printed in the terminal (usually `http://localhost:8501`).

## Database and logs
The SQLite database is created automatically in `data/expenses.db`. Application logs are stored in `logs/app.log`. These runtime files are excluded from Git.

## Deployment on Streamlit Community Cloud
1. Push this project to a public GitHub repository.
2. Sign in to Streamlit Community Cloud using GitHub.
3. Select **Create app** and choose your repository.
4. Set the main file path to `app.py`.
5. Deploy and copy the generated public app URL.

Note: Streamlit Community Cloud uses an ephemeral local filesystem in some deployment scenarios. For a long-term public app with persistent user data, connect a hosted database instead of relying on the local SQLite file.

## Demo video checklist
Record a 1-2 minute screen video showing:
1. The dashboard totals.
2. Adding one income transaction.
3. Adding one expense transaction.
4. The transaction history and CSV download.
5. The spending chart.

## Future improvements
- User login and authentication
- Hosted database for persistent cloud storage
- Budget limits and monthly alerts
- Edit transaction feature

## Author
Deepak Devtalla
