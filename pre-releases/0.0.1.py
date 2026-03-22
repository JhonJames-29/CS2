categories = {}
expenses = []

def set_budget():
    cat = input("Category: ")
    budget = float(input("Budget: "))
    categories[cat] = budget

def add_expense():
    cat = input("Category: ")
    amount = float(input("Expense amount: "))
    expenses.append({"cat": cat, "amt": amount})

def view_summary():
    print("\n--- Summary ---")
    total_spent = 0
    for cat, budget in categories.items():
        spent = sum(e["amt"] for e in expenses if e["cat"] == cat)
        total_spent += spent
        print(f"{cat}: Spent {spent} / Budget {budget}")
    print(f"Total spent: {total_spent}\n")

def main():
    while True:
        print("1. Set budget   2. Add expense   3. View summary   4. Quit")
        choice = input(">")
        if choice == "1": 
            set_budget()
        elif choice == "2": 
            add_expense()
        elif choice == "3": 
            view_summary()
        elif choice == "4": 
            break

main()