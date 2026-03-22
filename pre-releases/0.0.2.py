categories = {}
expenses = []

def set_budget():
    category = input("Enter category name: ")
    budget = float(input("Enter budget amount: "))
    categories[category] = budget

def add_expense():
    category = input("Enter category name: ")
    amount = float(input("Enter expense amount: "))
    expenses.append({"category": category, "amount": amount})

def view_summary():
    print("\n--- Budget Summary ---")
    total_spent = 0
    for category, budget in categories.items():
        spent = sum(e["amount"] for e in expenses if e["category"] == category)
        total_spent += spent
        print(f"{category}: Spent {spent} / Budget {budget}")
    print(f"Total spent: {total_spent}\n")

def main():
    while True:
        print("1. Set category budget  2. Add expense  3. View summary  4. Quit")
        choice = input("> ")
        if choice == "1": 
            set_budget()
        elif choice == "2": 
            add_expense()
        elif choice == "3": 
            view_summary()
        elif choice == "4": 
            break

main()
