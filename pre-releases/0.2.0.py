income = float(input("Enter your total income: "))
categories = {}
expenses = []

def set_budget():
    category = input("Enter category name: ")
    try:
        budget = float(input("Enter budget for this category: "))
        current_total = sum(categories.values()) + budget
        if current_total > income:
            print("!!! Cannot add! Total of all category budgets exceeds income.")
        else:
            categories[category] = budget
            print(f"Category '{category}' added with budget {budget}.")
    except ValueError:
        print("!!! Invalid input. Enter a number.")

def add_expense():
    category = input("Enter category name: ")
    if category not in categories:
        print("!!! Category does not exist.")
        return
    try:
        amount = float(input("Enter expense amount: "))
        expenses.append({"category": category, "amount": amount})
        if sum(e["amount"] for e in expenses if e["category"] == category) > categories[category]:
            print("!!! Warning: This category exceeded its budget!")
    except ValueError:
        print("!!! Invalid input. Enter a number.")

def add_income():
    global income
    try:
        amount = float(input("Enter additional income: "))
        income += amount
        print(f"Income updated! New total income: {income}")
    except ValueError:
        print("!!! Invalid input. Enter a number.")

def view_data():
    total_spent = sum(e["amount"] for e in expenses)
    total_remaining = income - total_spent
    print("\n--- Budget Summary ---")
    for category, budget in categories.items():
        spent = sum(e["amount"] for e in expenses if e["category"] == category)
        remaining = budget - spent
        print(f"{category}: Spent {spent} / Budget {budget} → Remaining {remaining}")
    print(f"\nTotal income: {income}")
    print(f"Total spent: {total_spent}")
    print(f"Total remaining money: {total_remaining}\n")

def main():
    while True:
        print("\n1. Set category budget  2. Add expense  3. View summary  4. Add income  5. Quit")
        choice = input(">")
        if choice == "1":
            set_budget()
        elif choice == "2":
            add_expense()
        elif choice == "3":
            view_data()
        elif choice == "4":
            add_income()
        elif choice == "5":
            break
        else:
            print("Invalid choice!")

main()