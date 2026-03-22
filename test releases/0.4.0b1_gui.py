import tkinter as tk
from tkinter import ttk, messagebox

#  DATA (same logic as version beta 0.4.0)
income = 0.0
categories = {}   # { name: budget }
expenses  = []    # [ {category, amount} ]


#  COLORS / STYLE
BG       = "#1e1e2e"   # dark background
PANEL    = "#2a2a3e"   # card background
ACCENT   = "#7c6af7"   # purple accent
GREEN    = "#4caf82"
RED      = "#e05c6a"
YELLOW   = "#f0c060"
FG       = "#e0e0f0"   # main text
MUTED    = "#888aaa"   # secondary text
FONT     = ("Segoe UI", 10)
FONT_B   = ("Segoe UI", 10, "bold")
FONT_H   = ("Segoe UI", 14, "bold")


#  HELPERS
def total_spent():
    return sum(e["amount"] for e in expenses)

def spent_in(cat):
    return sum(e["amount"] for e in expenses if e["category"] == cat)


#  MAIN APP
class BudgetApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Budget Tracker  v0.4.0b1_gui")
        self.geometry("680x520")
        self.resizable(False, False)
        self.configure(bg=BG)

        # ttk style
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TNotebook",          background=BG, borderwidth=0)
        style.configure("TNotebook.Tab",      background=PANEL, foreground=MUTED,
                        padding=[14, 6], font=FONT)
        style.map("TNotebook.Tab",
                  background=[("selected", ACCENT)],
                  foreground=[("selected", "#ffffff")])
        style.configure("TFrame",  background=BG)
        style.configure("TLabel",  background=BG, foreground=FG, font=FONT)
        style.configure("TEntry",  fieldbackground=PANEL, foreground=FG,
                        insertcolor=FG, font=FONT)
        style.configure("Treeview",
                        background=PANEL, foreground=FG,
                        fieldbackground=PANEL, rowheight=24, font=FONT)
        style.configure("Treeview.Heading",
                        background=ACCENT, foreground="#fff", font=FONT_B)
        style.map("Treeview", background=[("selected", ACCENT)])

        # build tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_dashboard = ttk.Frame(self.notebook)
        self.tab_budget    = ttk.Frame(self.notebook)
        self.tab_expense   = ttk.Frame(self.notebook)
        self.tab_help      = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_dashboard, text="  Dashboard  ")
        self.notebook.add(self.tab_budget,    text="  Budget  ")
        self.notebook.add(self.tab_expense,   text="  Expenses  ")
        self.notebook.add(self.tab_help,      text="  Help  ")

        self.build_dashboard()
        self.build_budget_tab()
        self.build_expense_tab()
        self.build_help_tab()

        # ask for income on first launch
        self.after(200, self.ask_income)

    # ── BUTTON FACTORY ───────────────────
    def btn(self, parent, text, cmd, color=ACCENT):
        return tk.Button(parent, text=text, command=cmd,
                         bg=color, fg="#fff", font=FONT_B,
                         relief="flat", cursor="hand2",
                         padx=12, pady=5,
                         activebackground=PANEL, activeforeground=FG)

    def label(self, parent, text, fg=FG, font=FONT):
        return tk.Label(parent, text=text, bg=BG, fg=fg, font=font)

    def entry(self, parent, width=26):
        e = tk.Entry(parent, bg=PANEL, fg=FG, insertbackground=FG,
                     font=FONT, relief="flat", width=width,
                     highlightthickness=1, highlightcolor=ACCENT,
                     highlightbackground=PANEL)
        return e


    #  TAB 1 — DASHBOARD
    def build_dashboard(self):
        p = self.tab_dashboard

        self.label(p, "Budget Tracker  v0.4.0b1_gui", fg=ACCENT, font=FONT_H).pack(pady=(18,4))
        self.label(p, "Test Release", fg=MUTED).pack()

        # summary cards row
        cards = tk.Frame(p, bg=BG)
        cards.pack(pady=14)

        self.lbl_income    = self._card(cards, "Income",    "$0.00", GREEN)
        self.lbl_spent     = self._card(cards, "Spent",     "$0.00", RED)
        self.lbl_remaining = self._card(cards, "Remaining", "$0.00", YELLOW)

        # add income row
        row = tk.Frame(p, bg=BG)
        row.pack(pady=6)
        self.label(row, "Add income: $").pack(side="left")
        self.inc_entry = self.entry(row, 14)
        self.inc_entry.pack(side="left", padx=6)
        self.btn(row, "Add", self.do_add_income, GREEN).pack(side="left")

        # category summary tree
        self.label(p, "Category Overview", fg=MUTED).pack(pady=(12,2))
        cols = ("Category", "Budget", "Spent", "Remaining")
        self.dash_tree = ttk.Treeview(p, columns=cols, show="headings", height=6)
        for c in cols:
            self.dash_tree.heading(c, text=c)
            self.dash_tree.column(c, width=148, anchor="center")
        self.dash_tree.pack(padx=14, fill="x")

    def _card(self, parent, title, value, color):
        f = tk.Frame(parent, bg=PANEL, padx=18, pady=10)
        f.pack(side="left", padx=8)
        tk.Label(f, text=title, bg=PANEL, fg=MUTED, font=FONT).pack()
        lbl = tk.Label(f, text=value, bg=PANEL, fg=color, font=FONT_H)
        lbl.pack()
        return lbl

    def refresh_dashboard(self):
        s = total_spent()
        r = income - s
        self.lbl_income.config(text=f"${income:.2f}")
        self.lbl_spent.config(text=f"${s:.2f}")
        self.lbl_remaining.config(text=f"${r:.2f}",
                                   fg=GREEN if r >= 0 else RED)
        # tree
        for row in self.dash_tree.get_children():
            self.dash_tree.delete(row)
        for cat, bud in categories.items():
            sp = spent_in(cat)
            rem = bud - sp
            tag = "over" if rem < 0 else "ok"
            self.dash_tree.insert("", "end",
                values=(cat, f"${bud:.2f}", f"${sp:.2f}", f"${rem:.2f}"),
                tags=(tag,))
        self.dash_tree.tag_configure("over", foreground=RED)
        self.dash_tree.tag_configure("ok",   foreground=FG)


    #  TAB 2 — BUDGET
    def build_budget_tab(self):
        p = self.tab_budget
        self.label(p, "Set Category Budget", fg=ACCENT, font=FONT_H).pack(pady=(18,14))

        form = tk.Frame(p, bg=BG)
        form.pack()

        self.label(form, "Category name:").grid(row=0, column=0, sticky="e", padx=8, pady=6)
        self.bud_cat = self.entry(form)
        self.bud_cat.grid(row=0, column=1, pady=6)

        self.label(form, "Budget amount ($):").grid(row=1, column=0, sticky="e", padx=8, pady=6)
        self.bud_amt = self.entry(form)
        self.bud_amt.grid(row=1, column=1, pady=6)

        self.btn(p, "  Set Budget  ", self.do_set_budget).pack(pady=10)

        self.label(p, "Existing Categories", fg=MUTED).pack(pady=(10,4))
        cols = ("Category", "Budget", "Spent", "Remaining")
        self.bud_tree = ttk.Treeview(p, columns=cols, show="headings", height=7)
        for c in cols:
            self.bud_tree.heading(c, text=c)
            self.bud_tree.column(c, width=148, anchor="center")
        self.bud_tree.pack(padx=14, fill="x")

    def refresh_budget_tree(self):
        for row in self.bud_tree.get_children():
            self.bud_tree.delete(row)
        for cat, bud in categories.items():
            sp = spent_in(cat)
            rem = bud - sp
            self.bud_tree.insert("", "end",
                values=(cat, f"${bud:.2f}", f"${sp:.2f}", f"${rem:.2f}"))


    #  TAB 3 — EXPENSES
    def build_expense_tab(self):
        p = self.tab_expense
        self.label(p, "Add Expense", fg=ACCENT, font=FONT_H).pack(pady=(18,14))

        form = tk.Frame(p, bg=BG)
        form.pack()

        self.label(form, "Category:").grid(row=0, column=0, sticky="e", padx=8, pady=6)
        self.exp_cat = self.entry(form)
        self.exp_cat.grid(row=0, column=1, pady=6)

        self.label(form, "Amount ($):").grid(row=1, column=0, sticky="e", padx=8, pady=6)
        self.exp_amt = self.entry(form)
        self.exp_amt.grid(row=1, column=1, pady=6)

        self.btn(p, "  Add Expense  ", self.do_add_expense).pack(pady=10)

        self.label(p, "Expense Log", fg=MUTED).pack(pady=(10,4))
        cols = ("#", "Category", "Amount")
        self.exp_tree = ttk.Treeview(p, columns=cols, show="headings", height=8)
        self.exp_tree.heading("#",        text="#")
        self.exp_tree.heading("Category", text="Category")
        self.exp_tree.heading("Amount",   text="Amount")
        self.exp_tree.column("#",         width=50,  anchor="center")
        self.exp_tree.column("Category",  width=280, anchor="w")
        self.exp_tree.column("Amount",    width=140, anchor="center")
        self.exp_tree.pack(padx=14, fill="x")

    def refresh_expense_tree(self):
        for row in self.exp_tree.get_children():
            self.exp_tree.delete(row)
        for i, e in enumerate(expenses, 1):
            self.exp_tree.insert("", "end",
                values=(i, e["category"], f"${e['amount']:.2f}"))


    #  TAB 4 — HELP
    def build_help_tab(self):
        p = self.tab_help
        self.label(p, "Help & Guide", fg=ACCENT, font=FONT_H).pack(pady=(18,10))

        # scrollable text area
        frame = tk.Frame(p, bg=BG)
        frame.pack(fill="both", expand=True, padx=16, pady=(0,14))

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        txt = tk.Text(frame, bg=PANEL, fg=FG, font=("Consolas", 10),
                      relief="flat", wrap="word", padx=12, pady=10,
                      yscrollcommand=scrollbar.set, state="normal",
                      highlightthickness=0)
        txt.pack(fill="both", expand=True)
        scrollbar.config(command=txt.yview)

        help_content = """\
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Budget Tracker  v0.4.0b1_gui  —  Quick Guide
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GETTING STARTED
───────────────
1. When the app opens, enter your total income in the popup.
2. Go to the Budget tab and create at least one category (e.g. Food, Transport).
3. Go to the Expenses tab to log your spending.
4. Check the Dashboard anytime for a summary.


DASHBOARD TAB
─────────────
• Shows your total Income, Amount Spent, and Remaining balance.
• "Add Income" lets you add extra income on top of your original amount.
• The Category Overview table shows each category's budget vs spending.
• Red rows mean you've gone over budget for that category!


BUDGET TAB
──────────
• Enter a category name (e.g. "Food") and a budget amount, then click Set Budget.
• The total of all category budgets cannot exceed your income.
• You can set as many categories as you need.


EXPENSES TAB
────────────
• Enter the category name (must match an existing one exactly).
• Enter the expense amount and click Add Expense.
• A warning pops up if you exceed a category's budget.
• All your expenses are listed in the log below.


TIPS
────
• Category names are case-sensitive: "food" ≠ "Food".
• You cannot add an expense to a category that doesn't exist yet.
• There is no save feature in this beta — data resets when you close the app.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  This is a test release (v0.4.0b1_gui).
  Logic is based from version beta 0.4.0,
  but with a new GUI built using Tkinter!
  Features like saving, editing, and reports
  are planned for future versions! :D
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        txt.insert("1.0", help_content)
        txt.config(state="disabled")


    #  ACTIONS
    def ask_income(self):
        dialog = tk.Toplevel(self)
        dialog.title("Set Income")
        dialog.geometry("320x160")
        dialog.configure(bg=BG)
        dialog.resizable(False, False)
        dialog.grab_set()

        tk.Label(dialog, text="Welcome to Budget Tracker!",
                 bg=BG, fg=ACCENT, font=FONT_B).pack(pady=(18,4))
        tk.Label(dialog, text="Enter your total income ($):",
                 bg=BG, fg=FG, font=FONT).pack()

        entry = tk.Entry(dialog, bg=PANEL, fg=FG, insertbackground=FG,
                         font=FONT, relief="flat", width=20,
                         highlightthickness=1, highlightcolor=ACCENT,
                         highlightbackground=PANEL)
        entry.pack(pady=8)
        entry.focus()

        def confirm(event=None):
            global income
            try:
                v = float(entry.get())
                if v <= 0:
                    raise ValueError
                income = v
                dialog.destroy()
                self.refresh_dashboard()
            except ValueError:
                messagebox.showerror("Invalid", "Please enter a positive number.")

        entry.bind("<Return>", confirm)
        tk.Button(dialog, text="Confirm", command=confirm,
                  bg=ACCENT, fg="#fff", font=FONT_B,
                  relief="flat", padx=12, pady=4).pack()

    def do_add_income(self):
        global income
        try:
            amt = float(self.inc_entry.get())
            if amt <= 0:
                raise ValueError
            income += amt
            self.inc_entry.delete(0, "end")
            self.refresh_dashboard()
            self.refresh_budget_tree()
        except ValueError:
            messagebox.showerror("Invalid", "Enter a valid positive amount.")

    def do_set_budget(self):
        cat = self.bud_cat.get().strip()
        if not cat:
            messagebox.showerror("Error", "Category name cannot be empty.")
            return
        try:
            amt = float(self.bud_amt.get())
            if amt <= 0:
                raise ValueError
            if sum(categories.values()) + amt > income:
                messagebox.showerror("Error",
                    "Cannot add! Total budgets would exceed income.")
                return
            categories[cat] = amt
            self.bud_cat.delete(0, "end")
            self.bud_amt.delete(0, "end")
            self.refresh_budget_tree()
            self.refresh_dashboard()
            messagebox.showinfo("Success", f"Category '{cat}' set to ${amt:.2f}")
        except ValueError:
            messagebox.showerror("Invalid", "Enter a valid positive amount.")

    def do_add_expense(self):
        cat = self.exp_cat.get().strip()
        if cat not in categories:
            messagebox.showerror("Error",
                f"Category '{cat}' doesn't exist.\nCreate it in the Budget tab first.")
            return
        try:
            amt = float(self.exp_amt.get())
            if amt <= 0:
                raise ValueError
            expenses.append({"category": cat, "amount": amt})
            self.exp_cat.delete(0, "end")
            self.exp_amt.delete(0, "end")
            self.refresh_expense_tree()
            self.refresh_dashboard()
            self.refresh_budget_tree()
            sp = spent_in(cat)
            if sp > categories[cat]:
                messagebox.showwarning("Budget Exceeded!",
                    f"⚠ You've gone over budget in '{cat}'!\n"
                    f"Budget: ${categories[cat]:.2f}  |  Spent: ${sp:.2f}")
        except ValueError:
            messagebox.showerror("Invalid", "Enter a valid positive amount.")


#  RUN
if __name__ == "__main__":
    app = BudgetApp()
    app.mainloop()