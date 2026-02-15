import json
import os
import time

SAVE_FILE = "budget_data.json"

def t(text, speed=0.02):
    comma_pause = speed * 2   
    stop_pause = speed * 5  
    
    for char in text:
        print(char, end="", flush=True)
        
        if char in (',', ';'):
            time.sleep(comma_pause)
        elif char in ('.', '?', '!'):
            time.sleep(stop_pause)
        else:
            time.sleep(speed)   
    print()

def color(text, c="32"): 
    return f"\033[{c}m{text}\033[0m"

income = 0
categories = {}
expenses = []

currentAutoSave = True 

def saveData(currentAutoSave):
    data = {
        "income": income,
        "categories": categories,
        "expenses": expenses,
        "autosave": currentAutoSave
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=4)
    t(color("✔ Data saved!", "36"))

def loadData():
    global income, categories, expenses, autosave
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            income = data.get("income", 0)
            categories = data.get("categories", {})
            expenses = data.get("expenses", [])
            autosave = data.get("autosave", True) 
        t(color("✔ Data loaded!", "36"))
    else:
        t(color("!!! No saved data found.", "33"))

def maybeSave(currentAutoSave):
    if currentAutoSave:
        saveData(currentAutoSave)

def inputFloat(prompt):
    try:
        value = float(input(prompt))
        if value < 0:
            t(color("!!! Negative numbers are not allowed!", "33"))
            return None
        return value
    except ValueError:
        t(color("!!! Invalid number!", "33"))
        return None

def setBudget():
    category = input("Enter category name: ")
    budget = inputFloat("Enter budget for this category: ")
    if budget is None:
        return
    if sum(categories.values()) + budget - categories.get(category, 0) > income:
        t(color("!!! Cannot add! Total category budgets exceed income.", "33"))
        return
    categories[category] = budget
    t(color(f"✔ Category '{category}' set with budget {budget}.", "36"))
    maybeSave(currentAutoSave)


def addExpense():
    category = input("Enter category: ")
    if category not in categories:
        t(color("!!! Category does not exist.", "33"))
        return
    amount = inputFloat("Enter expense amount: ")
    if amount is None:
        return
    expenses.append({"category": category, "amount": amount})
    spent = sum(e["amount"] for e in expenses if e["category"] == category)
    if spent > categories[category]:
        t(color("!!! Warning: Category overspent!", "31"))
    maybeSave(currentAutoSave)

def editCategory():
    category = input("Enter category to edit: ")
    if category not in categories:
        t(color("!!! Category not found.", "33"))
        return
    new_budget = inputFloat("Enter new budget: ")
    if new_budget is None:
        return
    if sum(categories.values()) - categories[category] + new_budget > income:
        t(color("!!! Cannot update! Total category budgets exceed income.", "33"))
        return
    categories[category] = new_budget
    t(color(f"✔ Category '{category}' updated.", "36"))
    maybeSave(currentAutoSave)

def deleteCategory():
    category = input("Enter category to delete: ")
    if category in categories:
        categories.pop(category)
        global expenses
        expenses = [e for e in expenses if e["category"] != category]
        t(color(f"✔ Category '{category}' and its expenses deleted.", "36"))
    else:
        t(color("!!! Category not found.", "33"))
    maybeSave(currentAutoSave)

def editExpense():
    if not expenses:
        t(color("!!! No expenses to edit.", "33"))
        return
    for i, e in enumerate(expenses):
        t(f"{i}: {e['category']} - {e['amount']}")
    try:
        idx = int(input("Enter expense number to edit: "))
        if 0 <= idx < len(expenses):
            new_amount = inputFloat("Enter new amount: ")
            if new_amount is not None:
                expenses[idx]["amount"] = new_amount
                t(color("✔ Expense updated.", "36"))
        else:
            t(color("!!! Invalid index.", "33"))
    except ValueError:
        t(color("!!! Invalid input.", "33"))
    maybeSave(currentAutoSave)

def deleteExpense():
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
    maybeSave(currentAutoSave)

def addIncome():
    global income
    amount = inputFloat("Enter additional income: ")
    if amount is not None:
        income += amount
        t(color(f"✔ Income updated! Total income: {income}", "36"))
    maybeSave(currentAutoSave)

def viewData():
    print(color("\n╔════════════════════════════════════════╗", "35"))
    t(color("║           Budget Tracker v1.3          ║", "35"))
    t(color("║               --Summary--              ║", "35"))
    print(color("╚════════════════════════════════════════╝", "35"))
    total_spent = sum(e["amount"] for e in expenses)
    for category, budget in categories.items():
        spent = sum(e["amount"] for e in expenses if e["category"] == category)
        remaining = budget - spent
        line = f"{category:<12} | Budget: {budget:<6} | Spent: {spent:<6} | Remaining: {remaining}"
        if remaining < 0:
            t(color(line, "31"))  
        else:
            t(line)
    print(color("========Overall=========", "34"))
    t(f"Total income:\t{income}")
    t(f"Total spent:\t{total_spent}")
    t(f"Remaining:\t{income - total_spent}")
    print(color("========================", "34"))

def viewChart():
    print(color("\n╔════════════════════════════════════════╗", "35"))
    t(color("║           Budget Tracker v1.3          ║", "35"))
    t(color("║       --Category Spending Chart--      ║", "35"))
    print(color("╚════════════════════════════════════════╝", "35"))

    if not categories:
        t(color("!!! No categories set yet.", "33"))
        return

    for category, budget in categories.items():
        spent = sum(e["amount"] for e in expenses if e["category"] == category)
        remaining = budget - spent
        percent = min(int((spent / budget) * 20), 20) if budget > 0 else 0
        bar = "█" * percent + "-" * (20 - percent)
        line = f"{category:<12} |{bar}| {spent}/{budget} | Remaining: {remaining}"
        
        if spent > budget:
            t(color(line, "31"))
        else:
            t(line)
    
    total_spent = sum(e["amount"] for e in expenses)
    print(color("========Overall=========", "34"))
    t(f"Total income:\t{income}")
    t(f"Total spent:\t{total_spent}")
    t(f"Remaining:\t{income - total_spent}")
    print(color("========================", "34"))


def main(currentAutoSave=True):
    loadData()
    while True:
        print(color("\n╔════════════════════════════════════════╗", "35"))
        t(color("║           Budget Tracker v1.3          ║", "35"))
        t(color("║              --Main Menu--             ║", "35"))
        t(color(f"║           --Auto-save is {'ON' if currentAutoSave else 'OFF'}--         ║", "35"))       
        print(color("╚════════════════════════════════════════╝", "35"))
        t(color("Setting up the budget:", "32"))
        print(color("\t[1] Set Category Budget", "32"))
        time.sleep(0.1)
        print(color("\t[2] Add Expense", "32"))
        time.sleep(0.1)
        print(color("\t[3] View Summary", "32"))
        time.sleep(0.1)
        print(color("\t[4] Add Income", "32"))
        time.sleep(0.1)
        t(color("Managing categories and expenses:", "33"))
        print(color("\t[5] Edit Category", "33"))
        time.sleep(0.1)
        print(color("\t[6] Delete Category", "33"))
        time.sleep(0.1)
        print(color("\t[7] Edit Expense", "33"))
        time.sleep(0.1)
        print(color("\t[8] Delete Expense", "33"))
        time.sleep(0.1)
        t(color("Data management:", "36"))
        print(color("\t[9] Save Data", "36"))
        time.sleep(0.1)
        print(color("\t[10] Load Data", "36"))
        time.sleep(0.1)
        print(color("\t[11] Auto-Save", "36"))
        time.sleep(0.1)
        print(color("\t[0] Quit", "31"))
        time.sleep(0.1)
        choice = input("> ")

        if choice == "1": 
            setBudget()
        elif choice == "2": 
            addExpense()
        elif choice == "3":
            print(color("\nView Options:\n\t[1] Summary\n\t[2] Chart", "36"))
            sub = input("> ")
            if sub == "1":
                viewData()
            elif sub == "2":
                viewChart()
            else:
                t(color("!!! Invalid choice!", "33"))
        elif choice == "4": 
            addIncome()
        elif choice == "5": 
            editCategory()
        elif choice == "6": 
            deleteCategory()
        elif choice == "7": 
            editExpense()
        elif choice == "8": 
            deleteExpense()
        elif choice == "9": 
            saveData(currentAutoSave)
        elif choice == "10": 
            loadData()
        elif choice == "11":
            t(color(f"\nAuto-save is currently {'ON' if currentAutoSave else 'OFF'}.", "36"))
            print(color("Toggle auto-save?: ", "36"))
            print(color("[y] Yes", "36"))
            print(color("[n] No", "31"))
            ans = input("> ").lower()
            if ans == "y":
                currentAutoSave = not currentAutoSave
                t(color(f"✔ Auto-save is now {'ON' if currentAutoSave else 'OFF'}.", "36"))
                saveData(currentAutoSave)
            else:
                t(color("✔ Auto-save state unchanged.", "36"))
        elif choice == "0": break
        else: t(color("\n!!! Invalid choice!", "33"))
    
    if currentAutoSave:
        saveData(currentAutoSave)

    t(color("✔ Exiting program. \tBuh-Byee! :D", "36"))
    time.sleep(1)

if __name__ == "__main__":
    main(currentAutoSave)
