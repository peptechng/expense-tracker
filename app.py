from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            amount REAL,
            category TEXT
        )
    """)
    conn.commit()
    conn.close()

# Main route
@app.route("/", methods=["GET", "POST"])
def index():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    if request.method == "POST":
        description = request.form["description"]
        amount = request.form["amount"]
        category = request.form["category"]

        cursor.execute(
            "INSERT INTO expenses (description, amount, category) VALUES (?, ?, ?)",
            (description, amount, category)
        )
        conn.commit()
        return redirect("/")

    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()
    total = sum(expense[2] for expense in expenses)
    conn.close()

    return render_template("index.html", expenses=expenses, total=total)

@app.route("/delete/<int:expense_id>")
def delete(expense_id):

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    conn.commit()

    conn.close()

    return redirect("/")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)