income = float(input("Enter your total income: "))
categories = {}
expenses = []

def loading():
    print("\n[Loading...]\n")

def set_budget():
    loading()
    category = input("Enter category name: ")
    try:
        budget = float(input("Enter budget: "))
        if sum(categories.values()) + budget > income:
            print("!!! Cannot add! Budgets exceed income.")
            return
        categories[category] = budget
        print(f"✔ Category '{category}' added.")
    except:
        print("!!! Invalid amount.")

def add_expense():
    loading()
    category = input("Enter category: ")
    if category not in categories:
        print("!!! Category does not exist.")
        return
    
    try:
        amount = float(input("Enter expense amount: "))
        expenses.append({"category": category, "amount": amount})
        spent = sum(e["amount"] for e in expenses if e["category"] == category)
        if spent > categories[category]:
            print("!!! WARNING: Budget exceeded!")
    except:
        print("!!! Invalid amount.")

def view_data():
    loading()
    print("╔═════════════════════════════════╗")
    print("║         BUDGET SUMMARY          ║")
    print("╚═════════════════════════════════╝")

    total_spent = sum(e["amount"] for e in expenses)

    for category, budget in categories.items():
        spent = sum(e["amount"] for e in expenses if e["category"] == category)
        remaining = budget - spent
        print(f"[{category}] Budget: {budget} | Spent: {spent} | Remaining: {remaining}")

    print("\n-------------------------------")
    print(f"Total income:   {income}")
    print(f"Total spent:    {total_spent}")
    print(f"Remaining:      {income - total_spent}")
    print("-------------------------------\n")

def main():
    while True:
        print("\n╔══════════════════════╗")
        print("║    Budget Tracker    ║")
        print("╚══════════════════════╝")
        print("[1] Set Category Budget")
        print("[2] Add Expense")
        print("[3] View Summary")
        print("[4] Add Income")
        print("[5] Quit")
        
        choice = input("> ")

        if choice == "1": 
            set_budget()
        elif choice == "2": 
            add_expense()
        elif choice == "3": 
            view_data()
        elif choice == "4":
            try:
                amt = float(input("Enter additional income: "))
                global income
                income += amt
            except:
                print("⚠️ Invalid amount.")
        elif choice == "5":
            break
        else:
            print("⚠ Invalid choice.")

main()
