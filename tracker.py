import sqlite3
from datetime import datetime

# Database Connection and Initialization
def init_db():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Add a New Expense
def add_expense(category, amount, description=""):
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    date_today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute('''
        INSERT INTO expenses (date, category, amount, description)
        VALUES (?, ?, ?, ?)
    ''', (date_today, category.capitalize(), amount, description))
    conn.commit()
    conn.close()
    print("\n✅ Expense successfully added!")

# View All Expenses
def view_expenses():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("\nℹ️ No expenses recorded yet.")
        return

    print("\n" + "="*60)
    print(f"{'ID':<4} | {'Date':<10} | {'Category':<15} | {'Amount (₹)':<10} | {'Description'}")
    print("="*60)
    for row in rows:
        print(f"{row[0]:<4} | {row[1]:<10} | {row[2]:<15} | {row[3]:<10.2f} | {row[4]}")
    print("="*60)

# Summary of Expenses (Total & Category-wise)
def view_summary():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    # Total spend
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0] or 0.0

    # Category-wise breakdown
    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    category_summary = cursor.fetchall()
    conn.close()

    print("\n" + "="*35)
    print("         EXPENSE SUMMARY         ")
    print("="*35)
    print(f"💰 Total Spent: ₹{total:.2f}\n")
    print("Category-wise Breakdown:")
    print("-" * 35)
    for category, sum_amt in category_summary:
        print(f"  • {category:<15}: ₹{sum_amt:.2f}")
    print("="*35)

# Delete an Expense
def delete_expense(expense_id):
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    if cursor.rowcount > 0:
        print(f"\n🗑️ Expense ID {expense_id} deleted successfully.")
    else:
        print("\n⚠️ Expense ID not found.")
    conn.commit()
    conn.close()

# Main Interactive Menu
def main():
    init_db()
    while True:
        print("\n--- 📊 PERSONAL EXPENSE TRACKER ---")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. View Expense Summary")
        print("4. Delete Expense")
        print("5. Exit")

        choice = input("Select an option (1-5): ").strip()

        if choice == '1':
            category = input("Category (e.g., Food, Transport, Rent): ").strip()
            try:
                amount = float(input("Amount (₹): "))
                description = input("Notes/Description (Optional): ").strip()
                add_expense(category, amount, description)
            except ValueError:
                print("\n❌ Invalid input! Amount must be a number.")

        elif choice == '2':
            view_expenses()

        elif choice == '3':
            view_summary()

        elif choice == '4':
            try:
                exp_id = int(input("Enter Expense ID to delete: "))
                delete_expense(exp_id)
            except ValueError:
                print("\n❌ Please enter a valid numerical ID.")

        elif choice == '5':
            print("\n👋 Exiting Expense Tracker. Have a great day!")
            break

        else:
            print("\n❌ Invalid choice! Please select 1, 2, 3, 4, or 5.")

if __name__ == "__main__":
    main()