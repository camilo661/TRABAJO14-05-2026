"""
customers.py
SQLite-backed local customer database.
Stores name, phone, email, frequent flag, and recharge history.
"""

import sqlite3
import os
import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "customers.db")


def _conn() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con


def init_db() -> None:
    """Create tables if they don't exist."""
    with _conn() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                phone TEXT PRIMARY KEY,
                name  TEXT NOT NULL,
                email TEXT NOT NULL,
                frequent INTEGER NOT NULL DEFAULT 0
            )
        """)
        con.execute("""
            CREATE TABLE IF NOT EXISTS recharges (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                phone        TEXT NOT NULL,
                timestamp    TEXT NOT NULL,
                operator     TEXT NOT NULL,
                plan_name    TEXT NOT NULL,
                plan_price   INTEGER NOT NULL,
                status       TEXT NOT NULL,
                FOREIGN KEY (phone) REFERENCES customers(phone)
            )
        """)


def upsert_customer(phone: str, name: str, email: str) -> None:
    """Insert or update a customer record (does NOT touch frequent flag)."""
    with _conn() as con:
        con.execute("""
            INSERT INTO customers (phone, name, email, frequent)
            VALUES (?, ?, ?, 0)
            ON CONFLICT(phone) DO UPDATE SET
                name  = excluded.name,
                email = excluded.email
        """, (phone, name, email))


def add_recharge(phone: str, operator: str, plan_name: str, plan_price: int, status: str) -> None:
    """Persist a completed recharge linked to the customer phone."""
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with _conn() as con:
        con.execute("""
            INSERT INTO recharges (phone, timestamp, operator, plan_name, plan_price, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (phone, ts, operator, plan_name, plan_price, status))


def get_customer(phone: str) -> dict | None:
    """Return customer dict or None."""
    with _conn() as con:
        row = con.execute("SELECT * FROM customers WHERE phone = ?", (phone,)).fetchone()
        return dict(row) if row else None


def search_customers(query: str) -> list[dict]:
    """Search by partial name or phone (case-insensitive). Returns list of dicts."""
    q = f"%{query}%"
    with _conn() as con:
        rows = con.execute(
            "SELECT * FROM customers WHERE name LIKE ? OR phone LIKE ? ORDER BY frequent DESC, name",
            (q, q)
        ).fetchall()
        return [dict(r) for r in rows]


def get_all_customers() -> list[dict]:
    with _conn() as con:
        rows = con.execute("SELECT * FROM customers ORDER BY frequent DESC, name").fetchall()
        return [dict(r) for r in rows]


def get_customer_recharges(phone: str) -> list[dict]:
    """Return all recharges for a customer, newest first."""
    with _conn() as con:
        rows = con.execute(
            "SELECT * FROM recharges WHERE phone = ? ORDER BY id DESC",
            (phone,)
        ).fetchall()
        return [dict(r) for r in rows]


def toggle_frequent(phone: str) -> bool:
    """Flip the frequent flag. Returns new value (True = frequent)."""
    with _conn() as con:
        row = con.execute("SELECT frequent FROM customers WHERE phone = ?", (phone,)).fetchone()
        if not row:
            return False
        new_val = 0 if row["frequent"] else 1
        con.execute("UPDATE customers SET frequent = ? WHERE phone = ?", (new_val, phone))
        return bool(new_val)


# Initialize on import
init_db()
