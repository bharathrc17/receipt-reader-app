import sqlite3
import pandas as pd
import os

os.makedirs("data", exist_ok=True)

conn = sqlite3.connect("data/receipts.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS receipts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vendor TEXT,
    date TEXT,
    amount REAL
)
''')
conn.commit()

# Insert a new receipt
def insert_receipt(vendor, date, amount):
    cursor.execute("INSERT INTO receipts (vendor, date, amount) VALUES (?, ?, ?)", (vendor, date, amount))
    conn.commit()

# Get all receipts with normalized column names
def get_all_receipts():
    df = pd.read_sql_query("SELECT * FROM receipts", conn)
    
    # Normalize column names to match expected casing
    df.rename(columns={
        "vendor": "Vendor",
        "date": "Date",
        "amount": "Amount"
    }, inplace=True)
    
    return df
