# Project Title: Budget Tracker

## Project Description

Budget Tracker is designed to help users manage their personal finances whilst being lightweight. It allows users to track income, set budgets for multiple  categories, record and manage expenses, and view clear summaries of their spending. 

Version 2.0 introduces major upgrades including password protection, recurring expenses, savings tracking, financial health indicators, backup systems, and enhanced reporting tools.

This program is suitable for beginners, students, or anyone looking for a simple way to understand their financial habits.

## Features: 

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

## Data Files:
- budget_data.json — Main data file
- budget_backup.json — Automatic backup file
- password.txt — Encrypted password storage

## New Implementations:

### Security
- Password protection on startup
- SHA-256 password hashing
- 3-attempt login limit
- Change password option
- Session authentication

### Savings & Financial Health (NEW in v2.0)
- Set savings goals
- Visual savings progress bar
- Automatic savings percentage calculation
- Financial health indicator:
    - 🟢 Healthy
    - 🟡 Caution
    - 🔴 Overspending
 
### Data Management
- Save and load using JSON (budget_data.json)
- Auto-save toggle
- Automatic backup creation (budget_backup.json)
- Restore from backup option
- Input validation for numbers and dates

## Prerequisite 

- Python 3.8 or higher
- Optional (for graphs): download the library "matplotlib" in command prompt:

      pip install matplotlib

## How to Run the Program:

1. Make sure Python is installed.
2. Download the latest release file.
3. Run the program in your terminal or IDE.
4. Follow on-screen prompts to manage, income, categories, and expenses.

**Notes:**
- Release v1.1 includes animated typing and color effects for an enhanced user experience.
- Release v1.2 includes the toggle of autosave, and includes an illustration of data by a graph.
- Release v1.3 includes fixing a data issue due to missing parameters for a trouble-free user experience.
- Release v2.0 includes new implementations that enhances user experience while maintaining security.

## Example Output: 

**Sample Data (from user input):**

    income = 2000

    categories = {
        "Food": 500,
        "Transport": 300,
        "Entertainment": 400,
        "Bills": 600
    }

**Dashboard Summary:**

    Income: $2000.00 | Spent: $1570.00 | Remaining: $430.00 | Health: █ Caution

**Category Overview:**

    Food         | Budget: 500.00 | Spent: 450.00 | Remain: 50.00  | 90.0%
    Transport    | Budget: 300.00 | Spent: 320.00 | Remain: -20.00 | 106.7%
    Entertainment| Budget: 400.00 | Spent: 200.00 | Remain: 200.00 | 50.0%
    Bills        | Budget: 600.00 | Spent: 600.00 | Remain: 0.00   | 100.0%


**Graph (Saving Progress):**

    Savings: [██████████████------] $430/$1000 (43%)

## Notes

- All data is saved locally in budget_data.json for persistence between sessions
- Future improvements may include: exporting reports (PDF or CSV), category-based percentages, and SQL implementations via sqlite3 library

## Contributers:

- Student 1: Sam Arquita  (encoded the program, did the changelog)  
- Student 2: Navine Bolo (gave the idea, wrote the readme)  
- Student 3: Ashley Makinano (made a rough Flowgorithm for version 0.0.1, made the proposal )
