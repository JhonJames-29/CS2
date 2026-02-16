# CHANGELOG

This file lists all the updates made to our Simple Budget Tracker project.

---

## Release v2.1 — Febuary 16, 2026

**Bugfix:**
Fixed: Data files now correctly load from BudgetTrackerData folder in user's home directory instead of current working directory

---

## Release v2.0 — February 13, 2026

The second major release of the Budget Tracker.

Key Notes:
Brand new implementations:

- Security System (New):
  - Password protection on startup
  - SHA-256 password hashing
  - 3-attempt login limit
  - Password change option
  - Session authentication
- Data Protection and Reliability
- Income and Savings Enhancments
  - Visual savings progress bar
  - Financial health indicator
- Cleaner UI

Difficulties:
- There may be times that the code will break due to circumstances that involves the password-related functions, the data-handling functions, and graphing functions. New releases will launch after such bugs will be fixed.

---

## Release v1.3 — November 30, 2025

Bugfix:
- Fixed an issue relating on saving the data due to missing parameters.

---

## Release v1.2 — November 29, 2025

Key Notes: 
New Features

- Auto-Save Functionality
- Spending Chart
  - Provides an easy-to-read snapshot of budget usage per category.
  - Overspending is highlighted in red.
- View Options Sub-Menu
  - Users can choose between:
    - Summary View: Classic detailed list of categories, budgets, spent, remaining.
    - Chart View: Graphical representation with bars for each category.

---

## Release v1.1 — November 23, 2025

Key Notes:
- All v1.0.0 functionality retained
- Typing effect for printing text 't()'
- Color coding for messages and warnings 'color()'
- Improved console experience for menus, summaries, and alerts
- Data still saved and loaded via JSON
- Minor interface polish

---

## Release v1.0 — November 20, 2025

The first release.

Features:
- Record total income and add additional income
- Set budgets for multiple categories '(food, tansport, entertainment, etc.)'
- Add and track expenses per category
- View per-category spending, total spent, and remaining money
- Overspending warnings when expenses exceed budgets
- Save and load all data using JSON 'budget_data.json'
- Clean and readable console interface with organized summary layout
- Input validation to prevent invalid entries
- Minor interface enhancements: ASCII borders, spacing, and loading prompts
- Edit / delete categories
- Edit / delete expenses

---

## Version v0.4.0 — August 28, 2025

Improvements:
- Introduced section borders and ASCII box headers for the summary screen
- Consistent spacing in menus for better readability
- Added simple loading animation for a polished feel
- Clearer warning messages
Notes / To-Do:
- Add JSON saving/loading
- Edit/delete categories and expenses
- Export summary to text files
- Percentage tracking per category
- Prepare for full UI overhaul

---

## Version v0.3.0 — August 20, 2025

Patchnotes:
- New menu layout for better clarity
- Better formatting of budget summary
- Improved text alignment for categories and amounts
- Small refactor of menu printing
Notes / To-Do:
- UI improvements
- JSON data saving
- Edit/delete functionality

---

## Version v0.2.1 — August 17, 2025

Key Notes:
- Added basic input validation for numbers
- Prevented negative budgets and expenses
- Cleaned printed messages
- Improved overspending warnings
Missing Features / To-Do:
- UI improvements
- JSON data saving
- Edit/delete functionality

---

## Version v0.2.0 — August 15, 2025

Improvements:  
A whole new different calculation. (Beta release)

- Now it depends on the income.  
- Income can be added.  
- Better overspending warnings.  
Notes:  
- Missing Features / To-Do:  
  - The use of JSON for saving data.  
  - Input validations to prevent crashes.  
  - Edit or delete categories and expenses.  
  - Better menu format

---

## Version v0.1.0 – August 15, 2025

- Alpha Stage:  
  - Added an error system such that it prints a warning whenever the `current_value` is more than the `total_budget` in `set_budget()`.  
  - Changed the whole system for comparing `total_budget` and `current_value`

---

## Version v0.0.2 – August 14, 2025

- Fixed naming variables to make the program readable.

---

## Version v0.0.1 – August 14, 2025

- The first version (Pre-Alpha stage) of the program.  
- The User can:  
  - Set a budget per category.  
  - Add expenses per category.  
  - View spendings per category and total spent.  
- Missing Features / To-Do:  
  - The use of JSON for saving data.  
  - Expenses can exceed the allocated budget without any warnings.  
  - Input validations to prevent crashes.  
  - Edit or delete categories and expenses.  
  - Advanced reports, or outputs.  
  - Better menu format

