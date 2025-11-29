# Project Title: Budget Tracker

## Project Description

Budget Tracker is designed to help users manage their personal finances whilst being lightweight. It allows users to track income, set budgets for multiple  categories, record and manage expenses, and view clear summaries of their spending. 

This program is suitable for beginners, students, or anyone looking for a simple way to understand their financial habits.

Features: 

- Record total income and add additional income
- Set budgets for multiple categories (food, transport, entertainment, etc.)
- Add and track expenses per category
- Edit and delete categories
- Edit and delete expenses
- View per-category spending, total spent, and remaining money
- Overspending warnings when expenses exceed budgets
- Save and load all data using JSON (budget_data.json)
- Clean and readable console interface with organized summary layout
- Input validation to prevent invalid entries
- Typing effect for dynamic text display
- Color-coded messages for warnings, confirmations, and summaries
- Polished menu and summary interface
- Category Spending Chart: Visual graph showing percentage of budget spent per category
- Save and load all data using JSON (budget_data.json)
- Auto-save feature: Automatically saves changes after

## How to Run the Program:

1. Make sure Python is installed.
2. Download the latest release file.
3. Run the program in your terminal or IDE.
4. Follow on-screen prompts to manage, income, categories, and expenses.

Note: Release v1.1 includes animated typing and color effects for an enhanced user experience.

## Example Output: 

**Sample Data (from .json):**

    income = 2000
    categories = {
        "Food": 500,
        "Transport": 300,
        "Entertainment": 400,
        "Bills": 600
    }
    expenses = [
        {"category": "Food", "amount": 450},
        {"category": "Transport", "amount": 320},
        {"category": "Entertainment", "amount": 200},
        {"category": "Bills", "amount": 600}
    ]

**Summary:**

    ╔════════════════════════════════════════╗
    ║           Budget Tracker v1.2          ║
    ║               --Summary--              ║
    ╚════════════════════════════════════════╝
    Food         | Budget: 500    | Spent: 450    | Remaining: 50
    Transport    | Budget: 300    | Spent: 320    | Remaining: -20
    Entertainment| Budget: 400    | Spent: 200    | Remaining: 200
    Bills        | Budget: 600    | Spent: 600    | Remaining: 0
    
    ========Overall=========
    Total income:   2000
    Total spent:    1570
    Remaining:      430
    ========================

**Graph**

    ╔════════════════════════════════════════╗
    ║           Budget Tracker v1.2          ║
    ║       --Category Spending Chart--      ║
    ╚════════════════════════════════════════╝

    Food         |████████████████----| 450/500
    Transport    |████████████████████| 320/300   <-- red, overspent
    Entertainment|██████████----------| 200/400
    Bills        |████████████████████| 600/600

    ========Overall=========
    Total income:   2000
    Total spent:    1570
    Remaining:      430
    ========================

## Notes

- All data is saved locally in budget_data.json for persistence between sessions
- Future improvements may include: exporting reports, advanced UI, and category-based percentages

## Contributers:

- Student 1: Sam Arquita  (encoded the program, did the changelog)  
- Student 2: Navine Bolo (gave the idea, wrote the readme)  
- Student 3: Ashley Makinano (made a rough Flowgorithm for version 0.0.1, made the proposal )
