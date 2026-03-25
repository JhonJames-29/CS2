# Budget Tracker!

---

## Project Description

Budget Tracker is designed to help users manage their personal finances whilst being lightweight. It allows users to track income, set budgets for multiple  categories, record and manage expenses, and view clear summaries of their spending. 

Version 2.0 introduces major upgrades including password protection, recurring expenses, savings tracking, financial health indicators, backup systems, and enhanced reporting tools.

Version 3.0 introduces major GUI and UX overhauls that replaced terminal-based UI with a full Tkinter GUI with 7 tabs: Dashboard, Budget, Expenses, Income & Savings, Reports, Settings, Help.

This program is suitable for beginners, students, or anyone looking for a simple way to understand their financial habits.

---

## Features: 

- Record total income and add additional income
- Set total income (replaces current value)
- Set budgets for multiple categories (`food`, `transport`, `entertainment`, etc.)
- Edit and delete categories
- Add and track expenses per category
- Edit and delete individual expenses
- Add recurring expenses with specified frequency (daily, weekly, monthly)
- Automatic application of recurring expenses on startup based on frequency
- View per-category spending, total spent, and remaining money
- Overspending warnings via GUI popups when expenses exceed budgets or reach 80% of budget
- View savings goal and track progress toward it
- Visual savings progress bar in the GUI showing percentage of goal achieved
- View monthly expenses and breakdown by category
- Search expenses by category or date range
- Financial health indicator (Healthy / Caution / Overspending)
- Graphical reports using matplotlib:
    - Category Spending Chart (Budget vs Spent per category)
    - Monthly Expense Trend
    - Pie charts for category breakdown
- Save and load all data using JSON (`budget_data.json`)
- Backup and restore data to prevent accidental loss (`budget_backup.json`, `budget_backup_[date].json`)
- Automatic backup rotation keeping the latest 5 backups
- Auto-save feature: Automatically saves changes when enabled
- Password protection with hashed passwords (SHA-256)
- Password masking during input
- Password change functionality
- Input validation for numeric values, dates, and non-empty strings
- Full GUI interface with 7 tabs: Dashboard, Budget, Expenses, Income & Savings, Reports, Settings, Help
- Login window that restricts access until authentication
- Clean and readable console interface with organized summary layout
- Color-coded messages for warnings, confirmations, and summaries
- Typing effect for dynamic text display *(Older versions only)*
- Polished menu interface with clear navigation
- Toggleable auto-save feature
- System-friendly for CLI (Windows and Unix-based systems) retained in background logic

---

## Data Files:
- budget_data.json — Main data file
- budget_backup.json — Automatic backup file (main)
    - budget_backup_[date] *(can be in multiple quantities)*— Automatic backup rotation keeping the latest 5 backups, while overwriting the main one.
- password.txt — Encrypted password storage
- password_hint.txt — A hint that the user provides
- expenses_export_[date].csv — A spreadsheet file (`.csv`) that converts the data *(from `budget_data.json`)* into a table. *(Optional file)*

## Data Structures:
**Data Storage Format (JSON):**

```json
{
    "income": 5000.0,
    "categories": {
        "Food": 600.0,
        "Rent": 1500.0,
        "Transportation": 300.0,
        "Entertainment": 200.0,
        "Utilities": 250.0,
        "Healthcare": 150.0,
        "Shopping": 300.0,
        "Savings": 500.0
    },
    "expenses": [
        {
            "category": "Rent",
            "amount": 1500.0,
            "date": "2026-02-01"
        },
        {
            "category": "Savings",
            "amount": 500.0,
            "date": "2026-02-01"
        },
        {
            "category": "Healthcare",
            "amount": 60.0,
            "date": "2026-02-11"
        },
        {
            "category": "Transportation",
            "amount": 48.0,
            "date": "2026-02-12"
        },
        {
            "category": "Rent",
            "amount": 1500.0,
            "date": "2026-03-22",
            "recurring": true
        },
        {
            "category": "Savings",
            "amount": 500.0,
            "date": "2026-03-22",
            "recurring": true
        },
        {
            "category": "Utilities",
            "amount": 50.0,
            "date": "2026-03-22",
            "recurring": true
        }
    ],
    "savings_goal": 3000.0,
    "recurring_expenses": [
        {
            "category": "Rent",
            "amount": 1500.0,
            "frequency_days": 30,
            "last_added": "2026-03-22"
        },
        {
            "category": "Savings",
            "amount": 500.0,
            "frequency_days": 30,
            "last_added": "2026-03-22"
        },
        {
            "category": "Utilities",
            "amount": 50.0,
            "frequency_days": 7,
            "last_added": "2026-03-22"
        }
    ],
    "income_history": [],
    "autosave": true
}
```

---

## New Implementations:

### Security
- Password protection on startup
- SHA-256 password hashing
- 3-attempt login limit
- Change password option
- Session authentication
- A password hint

### Savings & Financial Health
- Set savings goals
- Visual savings progress bar
- Automatic savings percentage calculation
- Financial health indicator:
    - 🟢 Healthy
    - 🟡 Caution
    - 🔴 Overspending
 
### Data Management
- Save and load using JSON (`budget_data.json`)
- Auto-save toggle
- Automatic backup creation (`budget_backup.json`)
- Restore from backup option
- Input validation for numbers and dates

---

> [!CAUTION]
> Hashed passwords are hard to retrieve. Forgetting the password would hinder the program useless as the required password was not given.

---

## Prerequisite/s: 

### If user used the python (.py) file:
The user must have:
- Python 3.8 or higher (Latest version is recommendable)
- Optional (for graphs): download the library "matplotlib" in command prompt (Win + R, "cmd.exe"):

```bash
pip install matplotlib
```

---

### If user used the python executable (.exe) file:
The user must have the operating system Windows 10/11 (As executable files are only compatible to Windows only.)

---

## How to Run the Program:

### (If a .py is used )

1. Make sure Python is installed.
2. Download the latest release file.
3. Run the program in your terminal or IDE.
4. Follow on-screen prompts to manage, income, categories, and expenses.

### (If a .exe is used)
1. Double tap the executable file
2. Follow on-screen prompts to manage, income, categories, and expenses.

---

# **Methodology:**

## 1. Implementation of Core Features
- The Budget Tracker system is developed in Python using an object-oriented design with a clean layered architecture. Key features in version 3.0 include:

    1. Income & Savings Management- The manipulation of total income, stored as a numeric attribute within the BudgetTracker class.
    2. Budget Category Management
    3. Expense Tracking
    4. Recurring Expense System
    5. Passowrd Authentication - Managed by `PasswordManager` with SHA-256 hashing, optional hint, three-attempt limit, and a full data-reset option.
    6. Data Persistence and Backup - Financial data is stored in a JSON file format for readability, storage, and easy access.
    7. Graph Integration - Data can be represented in a Graph.
    8. GUI with Tabs – The main window (BudgetApp) uses Tkinter with seven tabs: Dashboard, Budget, Expenses, Income & Savings, Reports, Settings, and Help.
    9. Financial Analytics

---

## 2. **Technologies used**
| Technology | Purpose | Justification |
| -------- | -------- | -------- |
| `Python` | Code development language. | Python uses simple, readable syntax which also includes a strong library support |
| `JSON` | Storage for data | A .json file is lightweight, readable, and does not require a database. |
| `hashlib` (SHA-256) | Used to hash passwords | A standard for hashing. |
| `Tkinter` | Graphical user interface | Built-in Python library for cross-platform GUIs, with support for windows, tabs, buttons, and dialogs |
| `tkinter.ttk` | Themed widgets | Provides advanced widgets like Treeview, Notebook (tabs), and Progressbars for a professional interface | 
| `tkinter.messagebox` | Popup dialogs | Allows info, warning, and error messages to the user |
| `os & shutil` | File management and backups | Handle file operations, directories, and backup rotations |
| `csv` | Export financial data | Allows easy export of data for external use or reporting |
| `datetime` | Handle dates and recurring expenses | Enables automatic date-stamping and recurring expense calculations |
| `matplotlib` | Data visualization | Widely used and reliable at plotting data as graphs. |
| `Pyinstaller` | Converts a `.py` file into an executable file (`.exe`) | Enables standalone distribution without requiring users to install Python. |

---

## 3. **Key Design Decisions and Trade-offs: (!RESPONSES FROM VERSION RELEASE 2.0!)**
- We decided to use JSON instead of an SQL Database as it is simple to setup and does not require an installation, but this won't allow us to scale up for large databases because the system only targets individual users.
- We used SHA-256 hashing for password storage. Although it is secure and lightweight, it is the only encryption layer for protecting passwords.
- We also developed the program as a CLI (Command Line Interface) application instead of a GUI (Graphical User Interface) application as it is lightweight and faster to develope. Although it is less visually interactive, the focus of the project is financial logic and simple data handling rather than graphicall interface design.
- Lastly, we've implemented the use of a toggleable auto-save feature. It prevents accidental data lass and improves reliability, but it slightly increase file write operations.

## 3. Key Design Decisions and Trade-offs (Updated for v3.0)
- We decided to continue using JSON instead of an SQL database because it is simple to set up and does not require installation, though it is not ideal for very large datasets; the system is still intended for individual users.
- We retained SHA-256 hashing for password storage. It is secure and lightweight, but it remains the only encryption layer for protecting passwords.
- The program was upgraded to a GUI (Graphical User Interface) using Tkinter instead of the previous CLI. This makes the app more visually interactive and user-friendly, though it adds complexity in development.
- We also implemented automatic data saving and backup. Autosave prevents accidental data loss and improves reliability, while a timestamped backup system ensures recovery. However, frequent saves slightly increase file write operations.
- Features like recurring expenses and financial dashboards were added, prioritizing automation and ease of monitoring over maintaining a minimal interface.

---

## **4. Ethical Considerations**
- User Privacy:
    - Passwords collected are hashed, not stored in plain text for encryption.
    - Financial data is stored locally.
    - No data is transmitted over the internet.
    - No third-party tracking is included (as the program is soly based on calculations done from the computer.)
- Data Protection
    - Backup system prevents accidental data loss during data cuorruption.
    - Input validation prevents corrupted entries or accidental entries.
    - Authentication (via password) limits unauthorize access.
- #### Responsible Use of AI Assistance ([Claude](https://claude.ai/login), [Anthropic](https://www.anthropic.com/))
> ##### &nbsp;&nbsp;&nbsp;&nbsp;"To refine the password handling mechanisms and optimize certain funtions, we used AI-assisted tools, more specifically, Claude and Claude Code. However, the overall system design, the structural decisions, knowing what libraries to use (library research), and the integration of the libraries we're independently performed by us! All major development decisions and final implementations were made based on personal understanding and evaluation."
> ##### &nbsp;&nbsp;&nbsp;&nbsp;"Claude is very smart at assistance, especially if the needed assistance involves coding. Since some features from our program is out of our knowledge, it was best to have assistance from Claude, as the AI is efficient, smart and solves problems that does not require any form of debugging. These tools were used as supplementary support for improving code structure, enhancing logic implementation, and addressing areas that required deeper technical refinement."
> ##### &nbsp;&nbsp;&nbsp;&nbsp;"While AI tools were used as an aid in development, they were not used as a replacement for learning or comprehension. Us, developers, ensured full understanding of the implemented code, maintaining academic integrity and responsible use of AI-assisted technologies."
> ##### &nbsp;&nbsp;&nbsp;&nbsp;"It's important to denote that despite we used AI, we shouldn't use it as a replacement. Understanding the code is also needed! :D"
> ###### _**"Sincerely,"**_<br/>_**"-Sam"**_

---

## **Notes to Consider:**
- Release v1.1 includes animated typing and color effects for an enhanced user experience.
- Release v1.2 includes the toggle of autosave, and includes an illustration of data by a graph.
- Release v1.3 includes fixing a data issue due to missing parameters for a trouble-free user experience.
- Release v2.0 includes new implementations that enhances user experience while maintaining security.
- Test Release v0.4.0b1_gui includes GUI implementations that drastically enhances user experience. Although not recommended for use, this serves as the foundation of the transition into a GUI based program. [Test Release Only!!!]
- Release v2.2's logic will be implemented to major release v3.0!
- Release v3.0 serves as an introduction to GUI's for succeeding versions! :D

---

## Example Output: 

**Sample Data (from user input): (!ONLY APPLICAPLE FROM VERSION RELEASE 2.0 OR BELOW!)**

```python
income = 2000
categories = {
    "Food": 500,
    "Transport": 300,
    "Entertainment": 400,
    "Bills": 600
}
expenses = [
    {"category": "Food", "amount": 450, "date": "2025-02-01"},
    {"category": "Transport", "amount": 320, "date": "2025-02-03"},
    {"category": "Entertainment", "amount": 200, "date": "2025-02-05"},
    {"category": "Bills", "amount": 600, "date": "2025-02-10"}
]
```
 
---    

**Dashboard Menu:**

```python
╔══════════════════════════════════════════════════════════╗
║  Budget Tracker v2.0                                     ║
║  MAIN DASHBOARD                                          ║
╚══════════════════════════════════════════════════════════╝

Income: $2000.00 | Spent: $1570.00 | Remaining: $430.00 | Health: █ Caution [YELLOW]

═══ BUDGET MANAGEMENT ═══
 1) Set Category Budget
 2) Edit Category Budget
 3) Delete Category
...
```
---

**Dashboard Summary:**

```python
Income: $2000.00 | Spent: $1570.00 | Remaining: $430.00 | Health: █ Caution [YELLOW]
```

---

**Category Overview:**

```python
CATEGORY STATUS
Food            | Budget: $500.00   | Spent: $450.00   | Remain: $50.00    |  90.0%
Transport       | Budget: $300.00   | Spent: $320.00   | Remain: $-20.00   | 106.7% [RED]
Entertainment   | Budget: $400.00   | Spent: $200.00   | Remain: $200.00   |  50.0%
Bills           | Budget: $600.00   | Spent: $600.00   | Remain: $0.00     | 100.0% [YELLOW]
    
TOTALS: Budget: $1800.00 | Spent: $1570.00
```

---

**Graph (Saving Progress):**

```python
Savings: [████████████████----] $430/$500 (86%)
```

---

**Monthly View (February 2025):**

```python
Expenses for 2025-02:

Food: $450.00
    2025-02-01 | $450

Transport: $320.00
    2025-02-03 | $320

Entertainment: $200.00
    2025-02-05 | $200

Bills: $600.00
    2025-02-10 | $600

Total spent: $1570.00
```

---

### **Release Notes**
Release v2.0 includes:

- Complete code refactoring and error fixes*
- Password protection system with SHA-256 hashing
- Recurring expense automation
- Monthly expense views with grouping
- Search functionality (by category or date range)
- Savings goal tracking with progress bar
- Financial health indicator
- Interactive graphs (category chart and monthly trend)
- Automatic backup system
- Session-based authentication
- Improved error handling and validation
- Better user interface with organized menus
-All previous features enhanced and stabilized

Release v2.2 includes: 

- Expense notes field — optional description on each expense
- View and Delete Recurring Expenses (options 8 & 9)
- Income history log with dates and notes
- Search expenses by amount range
- Category pie chart (option 20)
- CSV export to `~/BudgetTrackerData/`
- Rotating backups — keeps last 5 timestamped backup files
- Password hint — shown on last login attempt before lockout
- Password reset option after 3 failed attempts (wipes all data)
    
> [!NOTE]
> - All data is saved locally in budget_data.json for persistence between sessions
> - Future improvements may include: exporting reports (PDF or CSV), category-based percentages, and SQL implementations via sqlite3 library

## Security Considerations
- Passwords are hashed using SHA-256 (not stored in plain text)
- Password file should be kept secure
- JSON data files are not encrypted (for future enhancement)
- Session authentication prevents repeated password prompts

## Known Limitations
- Terminal colors may not work correctly on all terminals (Applicable from versions that are CLI-Based)
- Matplotlib is optional but required for graph features
- Password file is stored locally (not cloud-synced)
- Data persistence uses JSON files (not encrypted)
- Single-user system (no multi-user support)

---

## Contributers:

- Student 1: Sam Arquita 🐈 (encoded the program, did the changelog)  
- Student 2: Navine Bolo (gave the idea, wrote the readme)  
- Student 3: Ashley Makinano (made a rough Flowgorithm for version 0.0.1, made the proposal )

---

Our group !
<img width="1649" height="953" alt="67" src="https://github.com/user-attachments/assets/ac1a4d84-a590-4f1d-85bb-aa5d580eaa22" />
**Credits to Navine**
