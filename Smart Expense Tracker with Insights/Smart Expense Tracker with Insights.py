import json
import os
from datetime import datetime
from collections import defaultdict
import matplotlib.pyplot as plt

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

DATA_FILE = "expenses.json"


# ---------------------------
# Load Data
# ---------------------------
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as file:
        return json.load(file)


# ---------------------------
# Save Data
# ---------------------------
def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


# ---------------------------
# Add Expense
# ---------------------------
def add_expense():
    amount = float(input("Enter amount: "))
    category = input("Enter category (Food, Travel, Study, Other): ")
    note = input("Enter note: ")
    date = datetime.now().strftime("%Y-%m-%d")

    expense = {
        "amount": amount,
        "category": category,
        "note": note,
        "date": date
    }

    data = load_data()
    data.append(expense)
    save_data(data)

    print("✅ Expense added successfully!")


# ---------------------------
# View Expenses
# ---------------------------
def view_expenses():
    data = load_data()
    if not data:
        print("No expenses found.")
        return

    print("\n--- All Expenses ---")
    for exp in data:
        print(f"{exp['date']} | ₹{exp['amount']} | {exp['category']} | {exp['note']}")


# ---------------------------
# Monthly Trend Graph
# ---------------------------
def monthly_summary_graph():
    data = load_data()
    summary = defaultdict(float)

    for exp in data:
        month = exp["date"][:7]
        summary[month] += exp["amount"]

    if not summary:
        print("No data to display.")
        return

    months = list(summary.keys())
    totals = list(summary.values())

    plt.figure()
    plt.plot(months, totals, marker='o')
    plt.title("Monthly Expense Trend")
    plt.xlabel("Month")
    plt.ylabel("Total Spending")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# ---------------------------
# Category Pie Chart
# ---------------------------
def category_pie_chart():
    data = load_data()
    category_total = defaultdict(float)

    for exp in data:
        category_total[exp["category"]] += exp["amount"]

    if not category_total:
        print("No data to display.")
        return

    categories = list(category_total.keys())
    totals = list(category_total.values())

    plt.figure()
    plt.pie(totals, labels=categories, autopct='%1.1f%%')
    plt.title("Spending by Category")
    plt.show()


# ---------------------------
# PDF Report Generation
# ---------------------------
def generate_pdf_report():
    data = load_data()

    if not data:
        print("No data available to generate report.")
        return

    doc = SimpleDocTemplate("Expense_Report.pdf")
    styles = getSampleStyleSheet()
    content = []

    # Title
    content.append(Paragraph("Smart Expense Tracker Report", styles['Title']))
    content.append(Spacer(1, 20))

    total_expense = 0

    # Expense List
    for exp in data:
        line = f"{exp['date']} | ₹{exp['amount']} | {exp['category']} | {exp['note']}"
        content.append(Paragraph(line, styles['Normal']))
        content.append(Spacer(1, 10))
        total_expense += exp["amount"]

    content.append(Spacer(1, 20))
    content.append(Paragraph(f"Total Expense: ₹{total_expense}", styles['Heading2']))

    # Category Summary
    category_total = defaultdict(float)
    for exp in data:
        category_total[exp["category"]] += exp["amount"]

    content.append(Spacer(1, 20))
    content.append(Paragraph("Category Summary:", styles['Heading2']))

    for cat, amt in category_total.items():
        content.append(Paragraph(f"{cat}: ₹{amt}", styles['Normal']))

    doc.build(content)

    print("📄 PDF Report Generated: Expense_Report.pdf")


# ---------------------------
# Menu
# ---------------------------
def menu():
    while True:
        print("\n==== Smart Expense Tracker ====")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Monthly Trend Graph 📈")
        print("4. Category Pie Chart 🥧")
        print("5. Generate PDF Report 📄")
        print("6. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            monthly_summary_graph()
        elif choice == "4":
            category_pie_chart()
        elif choice == "5":
            generate_pdf_report()
        elif choice == "6":
            print("Goodbye 👋")
            break
        else:
            print("Invalid choice. Try again.")


# ---------------------------
# Run App
# ---------------------------
if __name__ == "__main__":
    menu()
