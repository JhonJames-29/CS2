categories = {}
expenses = []

def set_budget():
    category = input("Enter category name: ")
    budget = float(input("Enter budget for this category: "))

    total_budget = sum(categories.values())
    current_value = total_budget + budget

    if current_value > total_budget + budget:  
        print("!!! Warning: Budget exceeds previous total!")
        
    categories[category] = budget
    print(f"Category '{category}' added with budget {budget}.")

def add_expense():
    category = input("Enter category name: ")
    amount = float(input("Enter expense amount: "))
    expenses.append({"category": category, "amount": amount})

    spent = sum(e["amount"] for e in expenses if e["category"] == category)

    if spent > categories.get(category, 0):
        print("!!! Warning: You exceeded this category’s budget!")

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
