income = float(input("Enter your total income: "))
categories = {}
expenses = []

def get_float(prompt):
    try:
        value = float(input(prompt))
        if value < 0:
            print("!!! Negative numbers not allowed!")
            return None
        return value
    except ValueError:
        print("!!! Invalid number!")
        return None

def set_budget():
    category = input("Enter category name: ")
    budget = get_float("Enter budget: ")
    if budget is None: 
        return

    if sum(categories.values()) + budget > income:
        print("!!! Cannot add! Budgets exceed income.")
        return

    categories[category] = budget
    print(f"✔ Added category '{category}' with budget {budget}")

def add_expense():
    category = input("Enter category: ")
    if category not in categories:
        print("!!! Category does not exist.")
        return

    amount = get_float("Enter amount: ")
    if amount is None: return

    expenses.append({"category": category, "amount": amount})

    spent = sum(e["amount"] for e in expenses if e["category"] == category)
    if spent > categories[category]:
        print("!!! WARNING: Category overspent!")

def add_income():
    global income
    amount = get_float("Enter additional income: ")
    if amount is None: return
    income += amount
    print("✔ Income updated!")

def view_data():
    total_spent = sum(e["amount"] for e in expenses)
    print("\n--- Budget Summary ---")
    for category, budget in categories.items():
        spent = sum(e["amount"] for e in expenses if e["category"] == category)
        remaining = budget - spent
        print(f"{category}: {spent}/{budget} → Remaining {remaining}")
    print(f"\nTotal income: {income}")
    print(f"Total spent: {total_spent}")
    print(f"Remaining money: {income - total_spent}")

def main():
    while True:
        print("\n1.Set budget  2.Add expense  3.View summary  4.Add income   5.Quit")
        c = input("> ")
        if c == "1": 
            set_budget()
        elif c == "2": 
            add_expense()
        elif c == "3": 
            view_data()
        elif c == "4": 
            add_income()
        elif c == "5": 
            break
        else: 
            print("Invalid choice")

main()
