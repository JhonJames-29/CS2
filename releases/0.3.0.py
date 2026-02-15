income = float(input("Enter your total income: "))
categories = {}
expenses = []

def set_budget():
    category = input("Enter category name: ")
    try:
        budget = float(input("Enter budget for this category: "))
        if sum(categories.values()) + budget > income:
            print("!!! Cannot add! Budgets exceed income.")
            return
        categories[category] = budget
        print(f"✔ Category '{category}' added.")
    except:
        print("!!! Invalid number.")

def add_expense():
    category = input("Enter category name: ")
    if category not in categories:
        print("!!! Category does not exist.")
        return
    
    try:
        amount = float(input("Enter expense amount: "))
        expenses.append({"category": category, "amount": amount})
        spent = sum(e["amount"] for e in expenses if e["category"] == category)
        if spent > categories[category]:
            print("!!! Overspending alert!")
    except:
        print("!!! Invalid number.")

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
    while True:
        print("\n=== Budget Tracker ===")
        print("[1] Set Category Budget")
        print("[2] Add Expense")
        print("[3] View Summary")
        print("[4] Add Income")
        print("[5] Quit")
        print("======================")
        
        choice = input("> ")

        if choice == "1": 
            set_budget()
        elif choice == "2": 
            add_expense()
        elif choice == "3": 
            view_data()
        elif choice == "4":
            try:
                add_amt = float(input("Enter additional income: "))
                global income
                income += add_amt
            except:
                print("⚠️ Invalid number.")
        elif choice == "5":
            break
        else:
            print("⚠ Invalid choice.")

main()
