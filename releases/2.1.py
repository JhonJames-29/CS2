import json
import os
import sys
import time
from datetime import datetime, timedelta
import shutil
import hashlib

# Platform-specific imports for password masking
if os.name == 'nt':  # Windows
    import msvcrt
else:  # Unix/Linux/Mac
    import termios
    import tty

# Optional matplotlib import for graphs
try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("Note: matplotlib not installed. Graph features will be disabled.")
    print("To enable graphs, run: pip install matplotlib")


# ======== UTILITY FUNCTIONS ========

def getPasswordWithAsterisks(prompt="Enter password: "):
    """Get password input with asterisk masking"""
    print(prompt, end='', flush=True)
    password = ""
    
    if os.name == 'nt':  # Windows
        while True:
            char = msvcrt.getch()
            if char in (b'\r', b'\n'):  # Enter key
                print()
                break
            elif char == b'\x08':  # Backspace
                if len(password) > 0:
                    password = password[:-1]
                    sys.stdout.write('\b \b')
                    sys.stdout.flush()
            else:
                try:
                    password += char.decode('utf-8', errors='ignore')
                    sys.stdout.write('*')
                    sys.stdout.flush()
                except:
                    pass
    else:  # Unix/Linux/Mac
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                char = sys.stdin.read(1)
                if char in ('\n', '\r'):  # Enter key
                    print()
                    break
                elif char == '\x7f':  # Backspace
                    if len(password) > 0:
                        password = password[:-1]
                        sys.stdout.write('\b \b')
                        sys.stdout.flush()
                elif char == '\x03':  # Ctrl+C
                    raise KeyboardInterrupt
                else:
                    password += char
                    sys.stdout.write('*')
                    sys.stdout.flush()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    
    return password

def t(text, speed=0.01):
    """Type text with animation effect"""
    comma_pause = speed * 2
    stop_pause = speed * 5
    for char in str(text):
        print(char, end="", flush=True)
        if char in (',', ';'):
            time.sleep(comma_pause)
        elif char in ('.', '?', '!'):
            time.sleep(stop_pause)
        else:
            time.sleep(speed)
    print()

def color(text, c="32"):
    """Return colored text for terminal"""
    return f"\033[{c}m{text}\033[0m"

def clear():
    """Clear terminal screen"""
    os.system("cls" if os.name=="nt" else "clear")

def pause():
    """Pause and wait for user input"""
    input(color("\nPress Enter to continue...", "36"))

def inputFloat(prompt):
    """Get float input with validation"""
    try:
        value = float(input(prompt))
        if value < 0:
            print(color("!!! Negative numbers are not allowed!", "33"))
            return None
        return value
    except ValueError:
        print(color("!!! Invalid number!", "33"))
        return None

def inputInt(prompt):
    """Get integer input with validation"""
    try:
        value = int(input(prompt))
        if value < 0:
            print(color("!!! Negative numbers are not allowed!", "33"))
            return None
        return value
    except ValueError:
        print(color("!!! Invalid number!", "33"))
        return None

def validateDate(date_str):
    """Validate date format YYYY-MM-DD"""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def header(title):
    """Display formatted header"""
    print(color("╔" + "═" * 58 + "╗", "35"))
    print(color(f"║  Budget Tracker v2.0".ljust(59) + "║", "35"))
    print(color(f"║  {title}".ljust(59) + "║", "35"))
    print(color("╚" + "═" * 58 + "╝", "35"))


# ======== PASSWORD MANAGER CLASS ========

class PasswordManager:
    def __init__(self, password_file="password.txt"):
        base_dir = os.path.expanduser("~")  # User home folder
        data_dir = os.path.join(base_dir, "BudgetTrackerData")

        os.makedirs(data_dir, exist_ok=True)  # Create folder if missing

        self.password_file = os.path.join(data_dir, password_file)
        self.session_authenticated = False
    
    @staticmethod
    def hashPassword(password):
        """Hash a password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def setPassword(self, force=False):
        """Set a new password"""
        if os.path.exists(self.password_file) and not force:
            print(color("Password already exists. Use 'Change Password' option to change it.", "33"))
            return
        pw1 = getPasswordWithAsterisks("Enter new password: ")
        pw2 = getPasswordWithAsterisks("Confirm new password: ")
        if pw1 != pw2:
            print(color("!!! Passwords do not match.", "31"))
            return
        if len(pw1) < 4:
            print(color("!!! Password must be at least 4 characters.", "31"))
            return
        with open(self.password_file, "w") as f:
            f.write(self.hashPassword(pw1))
        print(color("✔ Password set.", "36"))
        self.session_authenticated = True
    
    def checkPassword(self):
        """Check password at startup"""
        # If already authenticated in this session, skip
        if self.session_authenticated:
            return True
        
        if not os.path.exists(self.password_file):
            print(color("No password set. Please create one.", "33"))
            self.setPassword()
            return True
        
        attempts = 3
        with open(self.password_file, "r") as f:
            saved_pw_hash = f.read().strip()
        
        while attempts > 0:
            pw = getPasswordWithAsterisks("Enter password: ")
            if self.hashPassword(pw) == saved_pw_hash:
                print(color("✔ Access granted.", "36"))
                self.session_authenticated = True
                return True
            else:
                attempts -= 1
                if attempts > 0:
                    print(color(f"!!! Wrong password! Attempts left: {attempts}", "31"))
        
        print(color("!!! Too many wrong attempts. Exiting...", "31"))
        sys.exit()
    
    def changePassword(self):
        """Change the existing password"""
        if not os.path.exists(self.password_file):
            print(color("!!! No password set yet.", "33"))
            return
        
        # Verify current password first
        with open(self.password_file, "r") as f:
            saved_pw_hash = f.read().strip()
        
        current_pw = getPasswordWithAsterisks("Enter current password: ")
        if self.hashPassword(current_pw) != saved_pw_hash:
            print(color("!!! Wrong password!", "31"))
            return
        
        # Set new password
        pw1 = getPasswordWithAsterisks("Enter new password: ")
        pw2 = getPasswordWithAsterisks("Confirm new password: ")
        if pw1 != pw2:
            print(color("!!! Passwords do not match.", "31"))
            return
        if len(pw1) < 4:
            print(color("!!! Password must be at least 4 characters.", "31"))
            return
        
        with open(self.password_file, "w") as f:
            f.write(self.hashPassword(pw1))
        print(color("✔ Password changed successfully.", "36"))


# ======== BUDGET TRACKER CLASS ========

class BudgetTracker:
    def __init__(self, save_file="budget_data.json", backup_file="budget_backup.json"):
        # Set up data directory (same as PasswordManager)
        base_dir = os.path.expanduser("~")  # User home folder
        data_dir = os.path.join(base_dir, "BudgetTrackerData")
        os.makedirs(data_dir, exist_ok=True)  # Create folder if missing
        
        self.save_file = os.path.join(data_dir, save_file)
        self.backup_file = os.path.join(data_dir, backup_file)
        
        # Data attributes
        self.income = 0
        self.categories = {}
        self.expenses = []
        self.savings_goal = 0
        self.recurring_expenses = []
        self.autosave = True
        
        # Password manager
        self.password_manager = PasswordManager()
    
    # ======== DATA MANAGEMENT ========
    
    def backupData(self):
        """Create backup of current data"""
        try:
            if os.path.exists(self.save_file):
                shutil.copy(self.save_file, self.backup_file)
                print(color("✔ Backup created.", "36"))
        except Exception as e:
            print(color(f"!!! Backup failed: {e}", "31"))
    
    def saveData(self):
        """Save all data to JSON file"""
        data = {
            "income": self.income,
            "categories": self.categories,
            "expenses": self.expenses,
            "savings_goal": self.savings_goal,
            "recurring_expenses": self.recurring_expenses,
            "autosave": self.autosave
        }
        try:
            with open(self.save_file, "w") as f:
                json.dump(data, f, indent=4)
            print(color("✔ Data saved!", "36"))
            self.backupData()
        except Exception as e:
            print(color(f"!!! Save failed: {e}", "31"))
    
    def loadData(self):
        """Load data from JSON file"""
        try:
            if os.path.exists(self.save_file):
                with open(self.save_file, "r") as f:
                    data = json.load(f)
                    self.income = data.get("income", 0)
                    self.categories = data.get("categories", {})
                    self.expenses = data.get("expenses", [])
                    self.savings_goal = data.get("savings_goal", 0)
                    self.recurring_expenses = data.get("recurring_expenses", [])
                    self.autosave = data.get("autosave", True)
                print(color("✔ Data loaded!", "36"))
            else:
                print(color("!!! No saved data found. Starting fresh.", "33"))
        except Exception as e:
            print(color(f"!!! Load failed: {e}", "31"))
            choice = input("Restore from backup? (y/n): ")
            if choice.lower() == 'y':
                self.restoreBackup()
    
    def restoreBackup(self):
        """Restore data from backup file"""
        if os.path.exists(self.backup_file):
            try:
                shutil.copy(self.backup_file, self.save_file)
                print(color("✔ Backup restored.", "36"))
                with open(self.save_file, "r") as f:
                    data = json.load(f)
                    self.income = data.get("income", 0)
                    self.categories = data.get("categories", {})
                    self.expenses = data.get("expenses", [])
                    self.savings_goal = data.get("savings_goal", 0)
                    self.recurring_expenses = data.get("recurring_expenses", [])
                    self.autosave = data.get("autosave", True)
                print(color("✔ Data loaded from backup!", "36"))
            except Exception as e:
                print(color(f"!!! Restore failed: {e}", "31"))
        else:
            print(color("!!! No backup available.", "33"))
    
    def maybeSave(self):
        """Save data if autosave is enabled"""
        if self.autosave:
            self.saveData()
    
    # ======== BUDGET MANAGEMENT ========
    
    def setBudget(self):
        """Set budget for a category"""
        category = input("Enter category name: ").strip()
        if not category:
            print(color("!!! Category name cannot be empty.", "33"))
            return
        budget = inputFloat("Enter budget: ")
        if budget is None: 
            return
        if sum(self.categories.values()) + budget - self.categories.get(category, 0) > self.income:
            print(color("!!! Warning: Total budgets exceed income.", "33"))
            proceed = input("Continue anyway? (y/n): ")
            if proceed.lower() != 'y':
                return
        self.categories[category] = budget
        print(color(f"✔ '{category}' set to {budget}", "36"))
        self.maybeSave()
    
    def editCategory(self):
        """Edit an existing category budget"""
        if not self.categories:
            print(color("!!! No categories to edit.", "33"))
            return
        category = input("Category to edit: ").strip()
        if category not in self.categories:
            print(color("!!! Category not found.", "33"))
            return
        new_budget = inputFloat("New budget: ")
        if new_budget is None: 
            return
        if sum(self.categories.values()) - self.categories[category] + new_budget > self.income:
            print(color("!!! Warning: Total budgets exceed income.", "33"))
            proceed = input("Continue anyway? (y/n): ")
            if proceed.lower() != 'y':
                return
        self.categories[category] = new_budget
        print(color(f"✔ '{category}' updated to {new_budget}", "36"))
        self.maybeSave()
    
    def deleteCategory(self):
        """Delete a category and its expenses"""
        if not self.categories:
            print(color("!!! No categories to delete.", "33"))
            return
        category = input("Category to delete: ").strip()
        if category in self.categories:
            confirm = input(f"Delete '{category}' and all its expenses? (y/n): ")
            if confirm.lower() != 'y':
                print(color("Cancelled.", "33"))
                return
            self.categories.pop(category)
            old_count = len(self.expenses)
            self.expenses = [e for e in self.expenses if e["category"] != category]
            removed_count = old_count - len(self.expenses)
            print(color(f"✔ '{category}' and {removed_count} expense(s) removed.", "36"))
        else:
            print(color("!!! Category not found.", "33"))
        self.maybeSave()
    
    # ======== EXPENSE MANAGEMENT ========
    
    def addExpense(self, recurring=False, category=None, amount=None):
        """Add an expense to a category"""
        if category is None:
            category = input("Enter category: ").strip()
        if category not in self.categories:
            print(color("!!! Category does not exist.", "33"))
            return
        if amount is None:
            amount = inputFloat("Enter amount: ")
        if amount is None: 
            return
        
        expense = {
            "category": category,
            "amount": amount,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "recurring": recurring
        }
        self.expenses.append(expense)
        spent = sum(e["amount"] for e in self.expenses if e["category"] == category)
        percent = spent / self.categories[category] if self.categories[category] > 0 else 0
        
        if percent >= 1: 
            print(color("!!! OVER BUDGET!", "31"))
        elif percent >= 0.8: 
            print(color("! Warning: 80% of budget used.", "33"))
        else:
            print(color(f"✔ Expense added. {percent*100:.1f}% of budget used.", "36"))
        
        self.maybeSave()
    
    def addRecurringExpense(self):
        """Add a recurring expense"""
        category = input("Category for recurring expense: ").strip()
        if category not in self.categories:
            print(color("!!! Category does not exist.", "33"))
            return
        amount = inputFloat("Amount: ")
        if amount is None: 
            return
        freq = inputFloat("Frequency in days: ")
        if freq is None or freq <= 0: 
            print(color("!!! Frequency must be greater than 0.", "33"))
            return
        
        self.recurring_expenses.append({
            "category": category,
            "amount": amount,
            "frequency_days": freq,
            "last_added": datetime.now().strftime("%Y-%m-%d")
        })
        print(color("✔ Recurring expense added", "36"))
        self.maybeSave()
    
    def applyRecurringExpenses(self):
        """Apply recurring expenses that are due"""
        today = datetime.now().date()
        applied = 0
        for r in self.recurring_expenses:
            try:
                last = datetime.strptime(r["last_added"], "%Y-%m-%d").date()
                if (today - last).days >= r["frequency_days"]:
                    # Add the expense automatically
                    expense = {
                        "category": r["category"],
                        "amount": r["amount"],
                        "date": today.strftime("%Y-%m-%d"),
                        "recurring": True
                    }
                    self.expenses.append(expense)
                    r["last_added"] = today.strftime("%Y-%m-%d")
                    applied += 1
            except Exception as e:
                print(color(f"!!! Error applying recurring expense: {e}", "31"))
        
        if applied > 0:
            print(color(f"✔ Applied {applied} recurring expense(s)", "36"))
            self.maybeSave()
    
    def editExpense(self):
        """Edit an existing expense"""
        if not self.expenses:
            print(color("!!! No expenses to edit.", "33"))
            return
        print(color("\nEXISTING EXPENSES:", "34"))
        for i, e in enumerate(self.expenses):
            print(f"{i}: {e['date']} | {e['category']} | ${e['amount']}")
        
        idx = inputInt("\nExpense number to edit: ")
        if idx is None or idx >= len(self.expenses):
            print(color("!!! Invalid index", "33"))
            return
        
        new_amount = inputFloat("New amount: ")
        if new_amount is not None:
            self.expenses[idx]["amount"] = new_amount
            print(color("✔ Expense updated", "36"))
            self.maybeSave()
    
    def deleteExpense(self):
        """Delete an expense"""
        if not self.expenses:
            print(color("!!! No expenses to delete.", "33"))
            return
        print(color("\nEXISTING EXPENSES:", "34"))
        for i, e in enumerate(self.expenses):
            print(f"{i}: {e['date']} | {e['category']} | ${e['amount']}")
        
        idx = inputInt("\nExpense number to delete: ")
        if idx is None or idx >= len(self.expenses):
            print(color("!!! Invalid index", "33"))
            return
        
        removed = self.expenses.pop(idx)
        print(color(f"✔ Removed {removed['category']} - ${removed['amount']}", "36"))
        self.maybeSave()
    
    # ======== INCOME & SAVINGS ========
    
    def addIncome(self):
        """Add to existing income"""
        amt = inputFloat("Enter income amount to add: ")
        if amt is not None:
            self.income += amt
            print(color(f"✔ Income updated: ${self.income}", "36"))
            self.maybeSave()
    
    def setIncome(self):
        """Set total income (replaces current value)"""
        amt = inputFloat("Enter total income: ")
        if amt is not None:
            self.income = amt
            print(color(f"✔ Total income set to: ${self.income}", "36"))
            self.maybeSave()
    
    def setSavingsGoal(self):
        """Set a savings goal"""
        goal = inputFloat("Enter savings goal: ")
        if goal is not None:
            self.savings_goal = goal
            print(color(f"✔ Savings goal set to ${self.savings_goal}", "36"))
            self.maybeSave()
    
    def viewSavingsProgress(self):
        """View progress toward savings goal"""
        total_spent = sum(e["amount"] for e in self.expenses)
        saved = self.income - total_spent
        if self.savings_goal == 0:
            print(color("No savings goal set.", "33"))
            print(f"Current savings: ${saved}")
            return
        percent = min(int((saved / self.savings_goal) * 100), 100) if saved > 0 else 0
        bar = "█" * (percent // 5) + "-" * (20 - percent // 5)
        print(f"Savings: [{bar}] ${saved}/${self.savings_goal} ({percent}%)")
        if saved >= self.savings_goal:
            print(color("🎉 Congratulations! You've reached your savings goal!", "32"))
        elif saved < 0:
            print(color("⚠ Warning: You're spending more than your income!", "31"))
    
    # ======== SEARCH & FILTERING ========
    
    def searchExpenses(self):
        """Search expenses by category or date range"""
        if not self.expenses:
            print(color("!!! No expenses to search.", "33"))
            return
        
        print("Search by:\n1) Category\n2) Date range (YYYY-MM-DD)")
        choice = input("> ").strip()
        results = []
        
        if choice == "1":
            cat = input("Enter category: ").strip()
            results = [e for e in self.expenses if e["category"] == cat]
        elif choice == "2":
            start = input("Start date (YYYY-MM-DD): ").strip()
            end = input("End date (YYYY-MM-DD): ").strip()
            
            if not validateDate(start) or not validateDate(end):
                print(color("!!! Invalid date format. Use YYYY-MM-DD", "33"))
                return
            
            results = [e for e in self.expenses if start <= e["date"] <= end]
        else:
            print(color("Invalid option", "33"))
            return
        
        if results:
            print(color(f"\nFound {len(results)} result(s):", "34"))
            total = 0
            for e in results:
                print(f"{e['date']} | {e['category']} | ${e['amount']}")
                total += e["amount"]
            print(color(f"\nTotal: ${total}", "36"))
        else:
            print(color("No results found.", "33"))
    
    # ======== VIEW FUNCTIONS ========
    
    def viewCategories(self):
        """View all categories with budget status"""
        print(color("\nCATEGORY STATUS", "34"))
        if not self.categories:
            print(color("No categories set.", "33"))
            return
        
        total_budget = sum(self.categories.values())
        total_spent = sum(e["amount"] for e in self.expenses)
        
        for cat, budget in sorted(self.categories.items()):
            spent = sum(e["amount"] for e in self.expenses if e["category"] == cat)
            remaining = budget - spent
            percent = spent / budget if budget > 0 else 0
            line = f"{cat:<15} | Budget: ${budget:<8.2f} | Spent: ${spent:<8.2f} | Remain: ${remaining:<8.2f} | {percent*100:5.1f}%"
            
            if percent >= 1: 
                print(color(line, "31"))
            elif percent >= 0.8: 
                print(color(line, "33"))
            else: 
                print(line)
        
        print(color(f"\nTOTALS: Budget: ${total_budget:.2f} | Spent: ${total_spent:.2f}", "34"))
    
    def viewMonthly(self):
        """View expenses for a specific month"""
        if not self.expenses:
            print(color("!!! No expenses to view.", "33"))
            return
        
        month = input("Enter month (YYYY-MM): ").strip()
        
        # Validate format
        try:
            datetime.strptime(month + "-01", "%Y-%m-%d")
        except ValueError:
            print(color("!!! Invalid format. Use YYYY-MM", "33"))
            return
        
        filtered = [e for e in self.expenses if e["date"].startswith(month)]
        if not filtered:
            print(color("No expenses found for this month.", "33"))
            return
        
        total = sum(e["amount"] for e in filtered)
        print(color(f"\nExpenses for {month}:", "34"))
        
        # Group by category
        by_category = {}
        for e in filtered:
            if e["category"] not in by_category:
                by_category[e["category"]] = []
            by_category[e["category"]].append(e)
        
        for cat in sorted(by_category.keys()):
            cat_total = sum(e["amount"] for e in by_category[cat])
            print(color(f"\n{cat}: ${cat_total:.2f}", "32"))
            for e in by_category[cat]:
                print(f"  {e['date']} | ${e['amount']}")
        
        print(color(f"\nTotal spent: ${total:.2f}", "36"))
    
    # ======== GRAPHS ========
    
    def plotCategoryChart(self):
        """Plot category spending vs budget chart"""
        if not MATPLOTLIB_AVAILABLE:
            print(color("!!! Graphs require matplotlib. Install with: pip install matplotlib", "31"))
            return
        
        if not self.categories:
            print(color("No categories to plot.", "33"))
            return
        
        names = list(self.categories.keys())
        spent_vals = [sum(e["amount"] for e in self.expenses if e["category"] == c) for c in names]
        budgets = [self.categories[c] for c in names]
        
        plt.figure(figsize=(12, 6))
        x = range(len(names))
        width = 0.35
        
        plt.bar([i - width/2 for i in x], budgets, width, color="lightblue", label="Budget", alpha=0.7)
        plt.bar([i + width/2 for i in x], spent_vals, width, color="green", label="Spent", alpha=0.7)
        
        plt.xlabel("Category")
        plt.ylabel("Amount ($)")
        plt.title("Category Spending vs Budget")
        plt.xticks(x, names, rotation=45, ha='right')
        plt.legend()
        plt.tight_layout()
        plt.show()
    
    def plotMonthlyTrend(self):
        """Plot monthly expense trend"""
        if not MATPLOTLIB_AVAILABLE:
            print(color("!!! Graphs require matplotlib. Install with: pip install matplotlib", "31"))
            return
        
        if not self.expenses:
            print(color("No expenses to plot.", "33"))
            return
        
        # Group by month
        month_totals = {}
        for e in self.expenses:
            month = e["date"][:7]  # YYYY-MM
            month_totals[month] = month_totals.get(month, 0) + e["amount"]
        
        months = sorted(month_totals.keys())
        totals = [month_totals[m] for m in months]
        
        plt.figure(figsize=(12, 6))
        plt.plot(months, totals, marker="o", linewidth=2, markersize=8)
        plt.xlabel("Month")
        plt.ylabel("Total Expenses ($)")
        plt.title("Monthly Expense Trend")
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
    
    # ======== FINANCIAL HEALTH ========
    
    def financialHealth(self):
        """Calculate and return financial health status"""
        if self.income == 0:
            return color("No income set", "33")
        
        total_spent = sum(e["amount"] for e in self.expenses)
        ratio = total_spent / self.income
        
        if ratio < 0.6:
            return color("█ Healthy", "32")
        elif ratio < 0.9:
            return color("█ Caution", "33")
        else:
            return color("█ Overspending", "31")
    
    # ======== MAIN LOOP ========
    
    def run(self):
        """Main application loop"""
        # Authenticate once at startup
        self.password_manager.checkPassword()
        self.loadData()
        
        while True:
            clear()
            self.applyRecurringExpenses()
            header("MAIN DASHBOARD")
            
            total_spent = sum(e["amount"] for e in self.expenses)
            remaining = self.income - total_spent
            
            print(color(f"\nIncome: ${self.income:.2f} | Spent: ${total_spent:.2f} | Remaining: ${remaining:.2f} | Health: {self.financialHealth()}", "34"))
            
            print(color("\n═══ BUDGET MANAGEMENT ═══", "32"))
            print(" 1) Set Category Budget")
            print(" 2) Edit Category Budget")
            print(" 3) Delete Category")
            
            print(color("\n═══ EXPENSES ═══", "32"))
            print(" 4) Add Expense")
            print(" 5) Edit Expense")
            print(" 6) Delete Expense")
            print(" 7) Add Recurring Expense")
            
            print(color("\n═══ INCOME & SAVINGS ═══", "32"))
            print(" 8) Add to Income")
            print(" 9) Set Total Income")
            print("10) Set Savings Goal")
            print("11) View Savings Progress")
              
            print(color("\n═══ REPORTS & VIEWS ═══", "32"))
            print("12) View Categories")
            print("13) View Monthly Expenses")
            print("14) Search Expenses")
            print("15) View Category Chart")
            print("16) View Monthly Trend")
            
            print(color("\n═══ SYSTEM ═══", "36"))
            print("17) Save Data")
            print("18) Load Data")
            print(f"19) Toggle Auto-Save [{'ON' if self.autosave else 'OFF'}]")
            print("20) Restore Backup")
            print("21) Change Password")
            print(" 0) Exit")
            
            choice = input("\nSelect > ").strip()
            
            if choice == "1": 
                clear(); header("SET CATEGORY"); self.setBudget(); pause()
            elif choice == "2": 
                clear(); header("EDIT CATEGORY"); self.editCategory(); pause()
            elif choice == "3": 
                clear(); header("DELETE CATEGORY"); self.deleteCategory(); pause()
            elif choice == "4": 
                clear(); header("ADD EXPENSE"); self.addExpense(); pause()
            elif choice == "5": 
                clear(); header("EDIT EXPENSE"); self.editExpense(); pause()
            elif choice == "6": 
                clear(); header("DELETE EXPENSE"); self.deleteExpense(); pause()
            elif choice == "7": 
                clear(); header("RECURRING EXPENSE"); self.addRecurringExpense(); pause()
            elif choice == "8": 
                clear(); header("ADD INCOME"); self.addIncome(); pause()
            elif choice == "9": 
                clear(); header("SET TOTAL INCOME"); self.setIncome(); pause()
            elif choice == "10": 
                clear(); header("SET SAVINGS GOAL"); self.setSavingsGoal(); pause()
            elif choice == "11": 
                clear(); header("SAVINGS PROGRESS"); self.viewSavingsProgress(); pause()
            elif choice == "12": 
                clear(); header("CATEGORIES"); self.viewCategories(); pause()
            elif choice == "13": 
                clear(); header("MONTHLY VIEW"); self.viewMonthly(); pause()
            elif choice == "14": 
                clear(); header("SEARCH EXPENSES"); self.searchExpenses(); pause()
            elif choice == "15": 
                self.plotCategoryChart(); pause()
            elif choice == "16": 
                self.plotMonthlyTrend(); pause()
            elif choice == "17": 
                self.saveData(); pause()
            elif choice == "18": 
                self.loadData(); pause()
            elif choice == "19": 
                self.autosave = not self.autosave
                print(color(f"Auto-save {'ON' if self.autosave else 'OFF'}", "36"))
                self.maybeSave()
                pause()
            elif choice == "20": 
                clear(); header("RESTORE BACKUP"); self.restoreBackup(); pause()
            elif choice == "21": 
                clear(); header("CHANGE PASSWORD"); self.password_manager.changePassword(); pause()
            elif choice == "0": 
                break
            else: 
                print(color("Invalid option", "33"))
                pause()
        
        if self.autosave: 
            self.saveData()
        print(color("✔ Exiting Budget Tracker v2.0", "36"))


# ======== MAIN ========

if __name__ == "__main__":
    tracker = BudgetTracker()
    tracker.run()