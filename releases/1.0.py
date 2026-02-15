import json
import os

SAVE_FILE = "budget_data.json"

income = 0
categories = {}
expenses = []

def save_data():
    data = {"income": income, "categories": categories, "expenses": expenses}
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=4)
    print("✔ Data saved!")

def load_data():
    global income, categories, expenses
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            income = data.get("income", 0)
            categories = data.get("categories", {})
            expenses = data.get("expenses", [])
        print("✔ Data loaded!")
    else:
        print("!!! No saved data found.")

def input_float(prompt):
    try:
        value = float(input(prompt))
        if value < 0:
            print("!!! Negative numbers are not allowed!")
            return None
        return value
    except ValueError:
        print("!!! Invalid number!")
        return None

def set_budget():
    category = input("Enter category name: ")
    budget = input_float("Enter budget for this category: ")
    if budget is None:
        return
    if sum(categories.values()) + budget - categories.get(category, 0) > income:
        print("!!! Cannot add! Total category budgets exceed income.")
        return
    categories[category] = budget
    print(f"✔ Category '{category}' set with budget {budget}.")

def add_expense():
    category = input("Enter category: ")
    if category not in categories:
        print("!!! Category does not exist.")
        return
    amount = input_float("Enter expense amount: ")
    if amount is None:
        return
    expenses.append({"category": category, "amount": amount})
    spent = sum(e["amount"] for e in expenses if e["category"] == category)
    if spent > categories[category]:
        print("!!! Warning: Category overspent!")

def edit_category():
    category = input("Enter category to edit: ")
    if category not in categories:
        print("!!! Category not found.")
        return
    new_budget = input_float("Enter new budget: ")
    if new_budget is None:
        return
    if sum(categories.values()) - categories[category] + new_budget > income:
        print("!!! Cannot update! Total category budgets exceed income.")
        return
    categories[category] = new_budget
    print(f"✔ Category '{category}' updated.")

def delete_category():
    category = input("Enter category to delete: ")
    if category in categories:
        categories.pop(category)
        global expenses
        expenses = [e for e in expenses if e["category"] != category]
        print(f"✔ Category '{category}' and its expenses deleted.")
    else:
        print("!!! Category not found.")

def edit_expense():
    if not expenses:
        print("!!! No expenses to edit.")
        return
    for i, e in enumerate(expenses):
        print(f"{i}: {e['category']} - {e['amount']}")
    try:
        idx = int(input("Enter expense number to edit: "))
        if 0 <= idx < len(expenses):
            new_amount = input_float("Enter new amount: ")
            if new_amount is not None:
                expenses[idx]["amount"] = new_amount
                print("✔ Expense updated.")
        else:
            print("!!! Invalid index.")
    except ValueError:
        print("!!! Invalid input.")

def delete_expense():
    if not expenses:
        print("!!! No expenses to delete.")
        return
    for i, e in enumerate(expenses):
        print(f"{i}: {e['category']} - {e['amount']}")
    try:
        idx = int(input("Enter expense number to delete: "))
        if 0 <= idx < len(expenses):
            removed = expenses.pop(idx)
            print(f"✔ Expense '{removed['category']} - {removed['amount']}' deleted.")
        else:
            print("!!! Invalid index.")
    except ValueError:
        print("!!! Invalid input.")

def add_income():
    global income
    amount = input_float("Enter additional income: ")
    if amount is not None:
        income += amount
        print(f"✔ Income updated! Total income: {income}")

def view_data():
    print("\n========================")
    print("      Budget Summary     ")
    print("========================")
    total_spent = sum(e["amount"] for e in expenses)
    for category, budget in categories.items():
        spent = sum(e["amount"] for e in expenses if e["category"] == category)
        remaining = budget - spent
        print(f"{category:<12} | Budget: {budget:<6} | Spent: {spent:<6} | Remaining: {remaining}")
    print("------------------------")
    print(f"Total income:   {income}")
    print(f"Total spent:    {total_spent}")
    print(f"Remaining:      {income - total_spent}")
    print("========================\n")

def main():
    load_data()
    while True:
        print("\n=== Budget Tracker v1.0 ===")
        print("[1] Set Category Budget")
        print("[2] Add Expense")
        print("[3] View Summary")
        print("[4] Add Income")
        print("[5] Edit Category")
        print("[6] Delete Category")
        print("[7] Edit Expense")
        print("[8] Delete Expense")
        print("[9] Save Data")
        print("[10] Load Data")
        print("[0] Quit")
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
        elif choice == "0": 
            break
        else: 
            print("!!! Invalid choice!")

    save_data()
    print("✔ Exiting program. Goodbye!")

main()
