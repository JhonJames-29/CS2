import json
import os
import time

SAVE_FILE = "budget_data.json"

def t(text, speed=0.02):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(speed)
    print()

def color(text, c="32"): 
    return f"\033[{c}m{text}\033[0m"

income = 0
categories = {}
expenses = []

def save_data():
    data = {"income": income, "categories": categories, "expenses": expenses}
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=4)
    t(color("✔ Data saved!", "36"))

def load_data():
    global income, categories, expenses
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            income = data.get("income", 0)
            categories = data.get("categories", {})
            expenses = data.get("expenses", [])
        t(color("✔ Data loaded!", "36"))
    else:
        t(color("!!! No saved data found.", "33"))

def input_float(prompt):
    try:
        value = float(input(prompt))
        if value < 0:
            t(color("!!! Negative numbers are not allowed!", "33"))
            return None
        return value
    except ValueError:
        t(color("!!! Invalid number!", "33"))
        return None

def set_budget():
    category = input("Enter category name: ")
    budget = input_float("Enter budget for this category: ")
    if budget is None:
        return
    if sum(categories.values()) + budget - categories.get(category, 0) > income:
        t(color("!!! Cannot add! Total category budgets exceed income.", "33"))
        return
    categories[category] = budget
    t(color(f"✔ Category '{category}' set with budget {budget}.", "36"))

def add_expense():
    category = input("Enter category: ")
    if category not in categories:
        t(color("!!! Category does not exist.", "33"))
        return
    amount = input_float("Enter expense amount: ")
    if amount is None:
        return
    expenses.append({"category": category, "amount": amount})
    spent = sum(e["amount"] for e in expenses if e["category"] == category)
    if spent > categories[category]:
        t(color("!!! Warning: Category overspent!", "31"))

def edit_category():
    category = input("Enter category to edit: ")
    if category not in categories:
        t(color("!!! Category not found.", "33"))
        return
    new_budget = input_float("Enter new budget: ")
    if new_budget is None:
        return
    if sum(categories.values()) - categories[category] + new_budget > income:
        t(color("!!! Cannot update! Total category budgets exceed income.", "33"))
        return
    categories[category] = new_budget
    t(color(f"✔ Category '{category}' updated.", "36"))

def delete_category():
    category = input("Enter category to delete: ")
    if category in categories:
        categories.pop(category)
        global expenses
        expenses = [e for e in expenses if e["category"] != category]
        t(color(f"✔ Category '{category}' and its expenses deleted.", "36"))
    else:
        t(color("!!! Category not found.", "33"))

def edit_expense():
    if not expenses:
        t(color("!!! No expenses to edit.", "33"))
        return
    for i, e in enumerate(expenses):
        t(f"{i}: {e['category']} - {e['amount']}")
    try:
        idx = int(input("Enter expense number to edit: "))
        if 0 <= idx < len(expenses):
            new_amount = input_float("Enter new amount: ")
            if new_amount is not None:
                expenses[idx]["amount"] = new_amount
                t(color("✔ Expense updated.", "36"))
        else:
            t(color("!!! Invalid index.", "33"))
    except ValueError:
        t(color("!!! Invalid input.", "33"))

def delete_expense():
    if not expenses:
        t(color("!!! No expenses to delete.", "33"))
        return
    for i, e in enumerate(expenses):
        t(f"{i}: {e['category']} - {e['amount']}")
    try:
        idx = int(input("Enter expense number to delete: "))
        if 0 <= idx < len(expenses):
            removed = expenses.pop(idx)
            t(color(f"✔ Expense '{removed['category']} - {removed['amount']}' deleted.", "36"))
        else:
            t(color("!!! Invalid index.", "33"))
    except ValueError:
        t(color("!!! Invalid input.", "33"))

def add_income():
    global income
    amount = input_float("Enter additional income: ")
    if amount is not None:
        income += amount
        t(color(f"✔ Income updated! Total income: {income}", "36"))

def view_data():
    t(color("\n========================", "34"))
    t(color("      Budget Summary     ", "34"))
    t(color("========================", "34"))
    total_spent = sum(e["amount"] for e in expenses)
    for category, budget in categories.items():
        spent = sum(e["amount"] for e in expenses if e["category"] == category)
        remaining = budget - spent
        line = f"{category:<12} | Budget: {budget:<6} | Spent: {spent:<6} | Remaining: {remaining}"
        if remaining < 0:
            t(color(line, "31"))  
        else:
            t(line)
    t(color("------------------------", "34"))
    t(f"Total income:   {income}")
    t(f"Total spent:    {total_spent}")
    t(f"Remaining:      {income - total_spent}")
    t(color("========================\n", "34"))

def main():
    load_data()
    while True:
        t(color("\n=== Budget Tracker v1.1 ===", "35"))
        print(color("[1] Set Category Budget", "32"))
        print(color("[2] Add Expense", "32"))
        print(color("[3] View Summary", "32"))
        print(color("[4] Add Income", "32"))
        print(color("[5] Edit Category", "33"))
        print(color("[6] Delete Category", "33"))
        print(color("[7] Edit Expense", "33"))
        print(color("[8] Delete Expense", "33"))
        print(color("[9] Save Data", "36"))
        print(color("[10] Load Data", "36"))
        print(color("[0] Quit", "31"))
        choice = input("> ")

        if choice == "1": 
            set_budget()
        elif choice == "2": 
            add_expense()
        elif choice == "3": 
            view_data()
        elif choice == "4": 
            add_income()
        elif choice == "5": 
            edit_category()
        elif choice == "6": 
            delete_category()
        elif choice == "7": 
            edit_expense()
        elif choice == "8": 
            delete_expense()
        elif choice == "9": 
            save_data()
        elif choice == "10": 
            load_data()
        elif choice == "0": break
        else: t(color("⚠ Invalid choice!", "33"))

    save_data()
    t(color("✔ Exiting program. Goodbye!", "36"))

main()
