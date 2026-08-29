import sqlite3
from datetime import datetime
from database.db import get_db


def get_user_by_id(user_id):
    conn = get_db()
    try:
        user = conn.execute(
            "SELECT name, email, created_at FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()
        if user is None:
            return None
        created_at = datetime.strptime(user["created_at"], "%Y-%m-%d %H:%M:%S")
        return {
            "name": user["name"],
            "email": user["email"],
            "member_since": created_at.strftime("%B %Y"),
        }
    finally:
        conn.close()


def get_recent_transactions(user_id, limit=10):
    conn = get_db()
    try:
        rows = conn.execute(
            "SELECT date, description, category, amount FROM expenses "
            "WHERE user_id = ? ORDER BY date DESC, id DESC LIMIT ?",
            (user_id, limit)
        ).fetchall()
        return [
            {
                "date": row["date"],
                "description": row["description"],
                "category": row["category"],
                "amount": f"\u20b9{row['amount']:.2f}",
            }
            for row in rows
        ]
    finally:
        conn.close()


def get_summary_stats(user_id):
    conn = get_db()
    try:
        row = conn.execute(
            "SELECT COALESCE(SUM(amount), 0) AS total, COUNT(*) AS cnt "
            "FROM expenses WHERE user_id = ?",
            (user_id,)
        ).fetchone()

        total_spent = f"\u20b9{row['total']:.2f}"
        transaction_count = row["cnt"]

        if transaction_count == 0:
            return {
                "total_spent": "\u20b90.00",
                "transaction_count": 0,
                "top_category": "\u2014",
            }

        top = conn.execute(
            "SELECT category, SUM(amount) AS cat_total "
            "FROM expenses WHERE user_id = ? "
            "GROUP BY category ORDER BY cat_total DESC LIMIT 1",
            (user_id,)
        ).fetchone()

        return {
            "total_spent": total_spent,
            "transaction_count": transaction_count,
            "top_category": top["category"],
        }
    finally:
        conn.close()


def get_category_breakdown(user_id):
    conn = get_db()
    try:
        rows = conn.execute(
            "SELECT category, SUM(amount) AS cat_total "
            "FROM expenses WHERE user_id = ? "
            "GROUP BY category ORDER BY cat_total DESC",
            (user_id,)
        ).fetchall()

        if not rows:
            return []

        grand_total = sum(row["cat_total"] for row in rows)
        if grand_total == 0:
            return []

        breakdown = []
        for row in rows:
            raw_pct = (row["cat_total"] / grand_total) * 100
            breakdown.append({
                "name": row["category"],
                "amount": f"\u20b9{row['cat_total']:.2f}",
                "pct": int(raw_pct),
            })

        pct_sum = sum(item["pct"] for item in breakdown)
        remainder = 100 - pct_sum
        if remainder != 0:
            breakdown[0]["pct"] += remainder

        return breakdown
    finally:
        conn.close()
