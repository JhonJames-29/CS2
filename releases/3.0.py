import json
import os
import sys
import hashlib
import shutil
import csv
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

try:
    import matplotlib
    matplotlib.use("TkAgg")
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

VERSION = "3.0"

#  THEME
BG     = "#10101A"
PANEL  = "#2a2a3e"
ACCENT = "#715df1"
GREEN  = "#4caf82"
RED    = "#e05c6a"
YELLOW = "#f0c060"
FG     = "#e0e0f0"
MUTED  = "#888aaa"
FONT   = ("Segoe UI", 10)
FONT_B = ("Segoe UI", 10, "bold")
FONT_H = ("Segoe UI", 13, "bold")
FONT_S = ("Segoe UI", 9)

DATA_DIR = os.path.join(os.path.expanduser("~"), "BudgetTrackerData")
os.makedirs(DATA_DIR, exist_ok=True)


#  WIDGET HELPERS


def make_btn(parent, text, cmd, color=ACCENT, width=None):
    kw = dict(bg=color, fg="#fff", font=FONT_B, relief="flat",
              cursor="hand2", padx=12, pady=5,
              activebackground=PANEL, activeforeground=FG)
    if width:
        kw["width"] = width
    return tk.Button(parent, text=text, command=cmd, **kw)


def make_lbl(parent, text, fg=FG, font=FONT, bg=BG):
    return tk.Label(parent, text=text, bg=bg, fg=fg, font=font)


def make_entry(parent, width=22, show=None):
    kw = dict(bg=PANEL, fg=FG, insertbackground=FG, font=FONT,
              relief="flat", width=width, highlightthickness=1,
              highlightcolor=ACCENT, highlightbackground=PANEL)
    if show:
        kw["show"] = show
    return tk.Entry(parent, **kw)


def make_tree(parent, cols, heights=8, col_widths=None):
    frame = tk.Frame(parent, bg=BG)
    sb = tk.Scrollbar(frame, bg=PANEL)
    sb.pack(side="right", fill="y")
    tree = ttk.Treeview(frame, columns=cols, show="headings",
                        height=heights, yscrollcommand=sb.set)
    sb.config(command=tree.yview)
    for i, c in enumerate(cols):
        tree.heading(c, text=c)
        w = col_widths[i] if col_widths else 120
        tree.column(c, width=w, anchor="center")
    tree.pack(side="left", fill="both", expand=True)
    return frame, tree


#  PASSWORD MANAGER


class PasswordManager:
    def __init__(self):
        self.pw_file   = os.path.join(DATA_DIR, "password.txt")
        self.hint_file = os.path.join(DATA_DIR, "password_hint.txt")

    @staticmethod
    def _hash(pw):
        return hashlib.sha256(pw.encode()).hexdigest()

    def has_password(self):
        return os.path.exists(self.pw_file)

    def check(self, pw):
        if not self.has_password():
            return False
        with open(self.pw_file) as f:
            return f.read().strip() == self._hash(pw)

    def set(self, pw):
        with open(self.pw_file, "w") as f:
            f.write(self._hash(pw))

    def set_hint(self, hint):
        if hint:
            with open(self.hint_file, "w") as f:
                f.write(hint)
        elif os.path.exists(self.hint_file):
            os.remove(self.hint_file)

    def get_hint(self):
        if os.path.exists(self.hint_file):
            with open(self.hint_file) as f:
                return f.read().strip()
        return ""

    def reset_all(self):
        for fn in os.listdir(DATA_DIR):
            try:
                os.remove(os.path.join(DATA_DIR, fn))
            except Exception:
                pass


#  DATA MANAGER

class DataManager:
    def __init__(self):
        self.save_file   = os.path.join(DATA_DIR, "budget_data.json")
        self.backup_file = os.path.join(DATA_DIR, "budget_backup.json")
        self.income          = 0.0
        self.categories      = {}
        self.expenses        = []
        self.savings_goal    = 0.0
        self.recurring       = []
        self.income_history  = []
        self.autosave        = True

    # ── Persistence ──────────────────────────

    def save(self, silent=False):
        data = {
            "income":            self.income,
            "categories":        self.categories,
            "expenses":          self.expenses,
            "savings_goal":      self.savings_goal,
            "recurring_expenses": self.recurring,
            "income_history":    self.income_history,
            "autosave":          self.autosave,
        }
        try:
            with open(self.save_file, "w") as f:
                json.dump(data, f, indent=4)
            self._make_backup()
            if not silent:
                messagebox.showinfo("Saved", "Data saved successfully.")
            return True
        except Exception as e:
            messagebox.showerror("Save Error", str(e))
            return False

    def _make_backup(self):
        try:
            if not os.path.exists(self.save_file):
                return
            ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            shutil.copy(self.save_file,
                        os.path.join(DATA_DIR, f"budget_backup_{ts}.json"))
            shutil.copy(self.save_file, self.backup_file)
            backups = sorted([
                f for f in os.listdir(DATA_DIR)
                if f.startswith("budget_backup_") and f.endswith(".json")
                and f != "budget_backup.json"
            ])
            for old in backups[:-5]:
                os.remove(os.path.join(DATA_DIR, old))
        except Exception:
            pass

    def load(self, silent=False):
        try:
            if not os.path.exists(self.save_file):
                if not silent:
                    messagebox.showinfo("Info", "No saved data found. Starting fresh.")
                return False
            with open(self.save_file) as f:
                data = json.load(f)
            self.income         = data.get("income", 0.0)
            self.categories     = data.get("categories", {})
            self.expenses       = data.get("expenses", [])
            self.savings_goal   = data.get("savings_goal", 0.0)
            self.recurring      = data.get("recurring_expenses", [])
            self.income_history = data.get("income_history", [])
            self.autosave       = data.get("autosave", True)
            if not silent:
                messagebox.showinfo("Loaded", "Data loaded successfully.")
            return True
        except Exception as e:
            messagebox.showerror("Load Error", str(e))
            return False

    def restore_backup(self):
        if not os.path.exists(self.backup_file):
            messagebox.showerror("Error", "No backup file found.")
            return False
        try:
            shutil.copy(self.backup_file, self.save_file)
            return self.load(silent=True)
        except Exception as e:
            messagebox.showerror("Restore Error", str(e))
            return False

    def maybe_save(self):
        if self.autosave:
            self.save(silent=True)

    def apply_recurring(self):
        today = datetime.now().date()
        applied = 0
        for r in self.recurring:
            try:
                last = datetime.strptime(r["last_added"], "%Y-%m-%d").date()
                if (today - last).days >= r["frequency_days"]:
                    self.expenses.append({
                        "category": r["category"],
                        "amount":   r["amount"],
                        "date":     today.strftime("%Y-%m-%d"),
                        "note":     "[Auto-Recurring]",
                        "recurring": True,
                    })
                    r["last_added"] = today.strftime("%Y-%m-%d")
                    applied += 1
            except Exception:
                pass
        if applied:
            self.maybe_save()
        return applied

    # ── Computed ──────────────────────────────

    def total_spent(self):
        return sum(e["amount"] for e in self.expenses)

    def spent_in(self, cat):
        return sum(e["amount"] for e in self.expenses if e["category"] == cat)

    def remaining(self):
        return self.income - self.total_spent()

    def health(self):
        if self.income == 0:
            return "No Income Set", MUTED
        ratio = self.total_spent() / self.income
        if ratio < 0.6:
            return "Healthy", GREEN
        elif ratio < 0.9:
            return "Caution", YELLOW
        return "Overspending", RED


#  LOGIN WINDOW

class LoginWindow(tk.Toplevel):
    def __init__(self, master, pm: PasswordManager, on_success):
        super().__init__(master)
        self.pm         = pm
        self.on_success = on_success
        self.attempts   = 3
        self.title(f"Budget Tracker v{VERSION} — Login")
        self.geometry("380x330")
        self.resizable(False, False)
        self.configure(bg=BG)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", sys.exit)
        self._build()

    def _build(self):
        make_lbl(self, f"Budget Tracker  v{VERSION}",
                 fg=ACCENT, font=("Segoe UI", 16, "bold")).pack(pady=(28, 2))
        make_lbl(self, "Personal Finance Manager",
                 fg=MUTED, font=FONT_S).pack()
        if not self.pm.has_password():
            self._build_create()
        else:
            self._build_login()

    # ── Login form ───────────────────────────

    def _build_login(self):
        make_lbl(self, "Enter your password:", fg=FG).pack(pady=(18, 4))
        hint = self.pm.get_hint()
        if hint:
            make_lbl(self, f"Hint: {hint}", fg=MUTED,
                     font=("Segoe UI", 9, "italic")).pack()

        self.pw_e = make_entry(self, width=24, show="*")
        self.pw_e.pack(pady=8)
        self.pw_e.focus()
        self.pw_e.bind("<Return>", lambda _: self._login())

        make_btn(self, "  Login  ", self._login).pack(pady=4)
        self.msg = make_lbl(self, "", fg=RED, font=FONT_S)
        self.msg.pack(pady=2)
        tk.Button(self, text="Forgot password? (resets all data)",
                  bg=BG, fg=MUTED, font=FONT_S, relief="flat",
                  cursor="hand2", command=self._reset_confirm).pack(pady=(8, 0))

    def _login(self):
        pw = self.pw_e.get()
        if self.pm.check(pw):
            self.destroy()
            self.on_success()
        else:
            self.attempts -= 1
            if self.attempts > 0:
                self.msg.config(
                    text=f"Wrong password. {self.attempts} attempt(s) left.")
                self.pw_e.delete(0, "end")
            else:
                self.msg.config(text="Too many failed attempts.")
                self.pw_e.config(state="disabled")

    # ── Create password form ─────────────────

    def _build_create(self):
        make_lbl(self, "Create a password to get started:", fg=FG).pack(pady=(18, 8))
        f = tk.Frame(self, bg=BG)
        f.pack()

        make_lbl(f, "Password:", bg=BG).grid(row=0, column=0, sticky="e", padx=8, pady=4)
        self.new_pw = make_entry(f, show="*")
        self.new_pw.grid(row=0, column=1, pady=4)

        make_lbl(f, "Confirm:", bg=BG).grid(row=1, column=0, sticky="e", padx=8, pady=4)
        self.conf_pw = make_entry(f, show="*")
        self.conf_pw.grid(row=1, column=1, pady=4)

        make_lbl(f, "Hint (opt):", bg=BG).grid(row=2, column=0, sticky="e", padx=8, pady=4)
        self.hint_e = make_entry(f)
        self.hint_e.grid(row=2, column=1, pady=4)

        self.new_pw.focus()
        make_btn(self, "  Create Password  ", self._create).pack(pady=10)
        self.msg = make_lbl(self, "", fg=RED, font=FONT_S)
        self.msg.pack()

    def _create(self):
        pw1 = self.new_pw.get()
        pw2 = self.conf_pw.get()
        if len(pw1) < 4:
            self.msg.config(text="Minimum 4 characters.")
            return
        if pw1 != pw2:
            self.msg.config(text="Passwords do not match.")
            return
        self.pm.set(pw1)
        self.pm.set_hint(self.hint_e.get().strip())
        self.destroy()
        self.on_success()

    def _reset_confirm(self):
        if messagebox.askyesno(
                "Reset All Data",
                "This will DELETE all saved data and reset your password.\n"
                "This cannot be undone. Are you sure?",
                parent=self):
            self.pm.reset_all()
            for w in self.winfo_children():
                w.destroy()
            # rebuild as create form
            make_lbl(self, f"Budget Tracker  v{VERSION}",
                     fg=ACCENT, font=("Segoe UI", 16, "bold")).pack(pady=(28, 2))
            make_lbl(self, "Personal Finance Manager",
                     fg=MUTED, font=FONT_S).pack()
            self._build_create()


#  MAIN APPLICATION

class BudgetApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.withdraw()          # hide until login completes
        self.title(f"Budget Tracker  v{VERSION}")
        self.geometry("940x670")
        self.minsize(820, 590)
        self.configure(bg=BG)

        self.pm = PasswordManager()
        self.dm = DataManager()

        self._setup_style()
        self._build_ui()

        LoginWindow(self, self.pm, self._after_login)

    # ── Post-login ────────────────────────────

    def _after_login(self):
        self.dm.load(silent=True)
        applied = self.dm.apply_recurring()
        self.deiconify()
        self.refresh_all()
        if applied:
            messagebox.showinfo(
                "Auto-Applied",
                f"{applied} recurring expense(s) were automatically applied today.")

    # ── ttk Style ────────────────────────────

    def _setup_style(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure("TNotebook",      background=BG,    borderwidth=0)
        s.configure("TNotebook.Tab",  background=PANEL, foreground=MUTED,
                    padding=[16, 7],  font=FONT)
        s.map("TNotebook.Tab",
              background=[("selected", ACCENT)],
              foreground=[("selected", "#fff")])
        s.configure("TFrame",  background=BG)
        s.configure("TLabel",  background=BG, foreground=FG, font=FONT)
        s.configure("Treeview",
                    background=PANEL, foreground=FG,
                    fieldbackground=PANEL, rowheight=26, font=FONT)
        s.configure("Treeview.Heading",
                    background=ACCENT, foreground="#fff", font=FONT_B)
        s.map("Treeview", background=[("selected", ACCENT)])
        s.configure("TSeparator", background=PANEL)
        s.configure("TProgressbar",
                    troughcolor=PANEL, background=ACCENT,
                    darkcolor=ACCENT,  lightcolor=ACCENT)

    # ── Build tabs ────────────────────────────

    def _build_ui(self):
        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=10, pady=10)
        self.nb = nb

        tabs = [
            ("tab_dash",     "  Dashboard  "),
            ("tab_budget",   "  Budget  "),
            ("tab_expense",  "  Expenses  "),
            ("tab_income",   "  Income & Savings  "),
            ("tab_reports",  "  Reports  "),
            ("tab_settings", "  Settings  "),
            ("tab_help",     "  Help  "),
        ]
        for attr, label in tabs:
            frame = ttk.Frame(nb)
            setattr(self, attr, frame)
            nb.add(frame, text=label)

        self._build_dashboard()
        self._build_budget()
        self._build_expense()
        self._build_income()
        self._build_reports()
        self._build_settings()
        self._build_help()

    #  TAB 1 — DASHBOARD

    def _build_dashboard(self):
        p = self.tab_dash

        make_lbl(p, f"Budget Tracker  v{VERSION}",
                 fg=ACCENT, font=("Segoe UI", 16, "bold")).pack(pady=(18, 2))
        make_lbl(p, "Personal Finance Manager", fg=MUTED, font=FONT_S).pack()

        # Summary cards
        cards = tk.Frame(p, bg=BG)
        cards.pack(pady=12)
        self.card_income    = self._card(cards, "Income",    "$0.00", GREEN)
        self.card_spent     = self._card(cards, "Spent",     "$0.00", RED)
        self.card_remaining = self._card(cards, "Remaining", "$0.00", YELLOW)
        self.card_health    = self._card(cards, "Health",    "N/A",   MUTED)

        # Savings progress
        sbar_f = tk.Frame(p, bg=BG)
        sbar_f.pack(pady=(4, 0))
        make_lbl(sbar_f, "Savings Goal:", fg=MUTED, font=FONT_S).pack(side="left", padx=4)
        self.dash_savings_lbl = make_lbl(sbar_f, "", fg=GREEN, font=FONT_S)
        self.dash_savings_lbl.pack(side="left")
        self.dash_progress = ttk.Progressbar(p, length=700, mode="determinate")
        self.dash_progress.pack(pady=4, padx=14)

        # Category overview
        make_lbl(p, "Category Overview", fg=MUTED, font=FONT_S).pack(pady=(8, 2))
        cols = ("Category", "Budget", "Spent", "Remaining", "Usage")
        widths = [180, 120, 120, 120, 90]
        tf, self.dash_tree = make_tree(p, cols, heights=8, col_widths=widths)
        tf.pack(fill="x", padx=14)

    def _card(self, parent, title, value, color):
        f = tk.Frame(parent, bg=PANEL, padx=20, pady=10)
        f.pack(side="left", padx=8)
        tk.Label(f, text=title, bg=PANEL, fg=MUTED, font=FONT_S).pack()
        lbl = tk.Label(f, text=value, bg=PANEL, fg=color, font=FONT_H)
        lbl.pack()
        return lbl

    def refresh_dashboard(self):
        dm = self.dm
        spent = dm.total_spent()
        rem   = dm.remaining()
        health_text, health_color = dm.health()

        self.card_income.config(text=f"${dm.income:.2f}")
        self.card_spent.config(text=f"${spent:.2f}")
        self.card_remaining.config(text=f"${rem:.2f}",
                                   fg=GREEN if rem >= 0 else RED)
        self.card_health.config(text=health_text, fg=health_color)

        if dm.savings_goal > 0:
            saved = max(0, rem)
            pct   = min(int(saved / dm.savings_goal * 100), 100)
            self.dash_progress["value"] = pct
            self.dash_savings_lbl.config(
                text=f"${saved:.2f} / ${dm.savings_goal:.2f}  ({pct}%)",
                fg=GREEN if pct >= 100 else YELLOW if pct >= 50 else FG)
        else:
            self.dash_progress["value"] = 0
            self.dash_savings_lbl.config(text="No goal set.", fg=MUTED)

        for row in self.dash_tree.get_children():
            self.dash_tree.delete(row)
        for cat, bud in dm.categories.items():
            sp  = dm.spent_in(cat)
            r   = bud - sp
            pct = sp / bud * 100 if bud > 0 else 0
            tag = "over" if r < 0 else "warn" if pct >= 80 else "ok"
            self.dash_tree.insert("", "end",
                values=(cat, f"${bud:.2f}", f"${sp:.2f}",
                        f"${r:.2f}", f"{pct:.1f}%"),
                tags=(tag,))
        self.dash_tree.tag_configure("over", foreground=RED)
        self.dash_tree.tag_configure("warn", foreground=YELLOW)
        self.dash_tree.tag_configure("ok",   foreground=FG)

    #  TAB 2 — BUDGET

    def _build_budget(self):
        p = self.tab_budget
        make_lbl(p, "Budget Management", fg=ACCENT, font=FONT_H).pack(pady=(16, 12))

        form = tk.Frame(p, bg=BG)
        form.pack()
        make_lbl(form, "Category name:", bg=BG).grid(
            row=0, column=0, sticky="e", padx=8, pady=5)
        self.bud_cat = make_entry(form)
        self.bud_cat.grid(row=0, column=1, pady=5)
        make_lbl(form, "Budget amount ($):", bg=BG).grid(
            row=1, column=0, sticky="e", padx=8, pady=5)
        self.bud_amt = make_entry(form)
        self.bud_amt.grid(row=1, column=1, pady=5)

        btn_row = tk.Frame(p, bg=BG)
        btn_row.pack(pady=8)
        make_btn(btn_row, "Set / Update Budget",
                 self._do_set_budget).pack(side="left", padx=4)
        make_btn(btn_row, "Edit Selected",
                 self._do_edit_category, YELLOW).pack(side="left", padx=4)
        make_btn(btn_row, "Delete Selected",
                 self._do_delete_category, RED).pack(side="left", padx=4)

        make_lbl(p, "Existing Categories", fg=MUTED, font=FONT_S).pack(pady=(8, 2))
        cols = ("Category", "Budget", "Spent", "Remaining", "Usage")
        widths = [200, 120, 120, 120, 90]
        tf, self.bud_tree = make_tree(p, cols, heights=10, col_widths=widths)
        tf.pack(fill="both", expand=True, padx=14, pady=(0, 10))

    def refresh_budget(self):
        for row in self.bud_tree.get_children():
            self.bud_tree.delete(row)
        dm = self.dm
        for cat, bud in dm.categories.items():
            sp  = dm.spent_in(cat)
            rem = bud - sp
            pct = sp / bud * 100 if bud > 0 else 0
            tag = "over" if rem < 0 else "warn" if pct >= 80 else "ok"
            self.bud_tree.insert("", "end",
                values=(cat, f"${bud:.2f}", f"${sp:.2f}",
                        f"${rem:.2f}", f"{pct:.1f}%"),
                tags=(tag,))
        self.bud_tree.tag_configure("over", foreground=RED)
        self.bud_tree.tag_configure("warn", foreground=YELLOW)
        self.bud_tree.tag_configure("ok",   foreground=FG)
        # keep expense category dropdown in sync
        self.exp_cat_combo["values"] = list(dm.categories.keys())

    def _do_set_budget(self):
        cat = self.bud_cat.get().strip()
        if not cat:
            messagebox.showerror("Error", "Category name cannot be empty.")
            return
        try:
            amt = float(self.bud_amt.get())
            if amt < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Enter a valid non-negative amount.")
            return
        current_total = sum(self.dm.categories.values())
        old_budget    = self.dm.categories.get(cat, 0)
        new_total     = current_total - old_budget + amt
        if new_total > self.dm.income and self.dm.income > 0:
            if not messagebox.askyesno(
                    "Warning",
                    f"Total budgets (${new_total:.2f}) exceed income "
                    f"(${self.dm.income:.2f}).\nContinue anyway?"):
                return
        self.dm.categories[cat] = amt
        self.bud_cat.delete(0, "end")
        self.bud_amt.delete(0, "end")
        self.dm.maybe_save()
        self.refresh_all()
        messagebox.showinfo("Success", f"'{cat}' budget set to ${amt:.2f}")

    def _do_edit_category(self):
        sel = self.bud_tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Select a category to edit.")
            return
        cat = self.bud_tree.item(sel[0])["values"][0]
        self.bud_cat.delete(0, "end")
        self.bud_cat.insert(0, cat)
        self.bud_amt.delete(0, "end")
        self.bud_amt.insert(0, str(self.dm.categories[cat]))
        messagebox.showinfo(
            "Edit",
            f"'{cat}' pre-filled in the form.\nAdjust the amount and click 'Set / Update Budget'.")

    def _do_delete_category(self):
        sel = self.bud_tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Select a category to delete.")
            return
        cat   = self.bud_tree.item(sel[0])["values"][0]
        count = sum(1 for e in self.dm.expenses if e["category"] == cat)
        if not messagebox.askyesno(
                "Confirm Delete",
                f"Delete '{cat}' and its {count} expense(s)?\nThis cannot be undone."):
            return
        self.dm.categories.pop(cat, None)
        self.dm.expenses = [e for e in self.dm.expenses if e["category"] != cat]
        self.dm.maybe_save()
        self.refresh_all()

    #  TAB 3 — EXPENSES

    def _build_expense(self):
        p = self.tab_expense
        make_lbl(p, "Expense Tracker", fg=ACCENT, font=FONT_H).pack(pady=(14, 8))

        # Add expense form
        form = tk.Frame(p, bg=BG)
        form.pack()
        make_lbl(form, "Category:", bg=BG).grid(row=0, column=0, sticky="e", padx=8, pady=4)
        self.exp_cat_combo = ttk.Combobox(form, width=20, font=FONT, state="readonly")
        self.exp_cat_combo.grid(row=0, column=1, pady=4, sticky="w")

        make_lbl(form, "Amount ($):", bg=BG).grid(row=0, column=2, sticky="e", padx=8, pady=4)
        self.exp_amt = make_entry(form, width=14)
        self.exp_amt.grid(row=0, column=3, pady=4)

        make_lbl(form, "Note (opt):", bg=BG).grid(row=1, column=0, sticky="e", padx=8, pady=4)
        self.exp_note = make_entry(form, width=50)
        self.exp_note.grid(row=1, column=1, columnspan=3, pady=4, sticky="w")

        btn_row = tk.Frame(p, bg=BG)
        btn_row.pack(pady=5)
        make_btn(btn_row, "Add Expense",
                 self._do_add_expense).pack(side="left", padx=4)
        make_btn(btn_row, "Edit Selected",
                 self._do_edit_expense, YELLOW).pack(side="left", padx=4)
        make_btn(btn_row, "Delete Selected",
                 self._do_delete_expense, RED).pack(side="left", padx=4)

        make_lbl(p, "Expense Log", fg=MUTED, font=FONT_S).pack(pady=(4, 2))
        cols = ("#", "Date", "Category", "Amount", "Note", "Rec?")
        widths = [40, 90, 150, 90, 240, 50]
        tf, self.exp_tree = make_tree(p, cols, heights=7, col_widths=widths)
        tf.pack(fill="x", padx=14)

        # Recurring section
        ttk.Separator(p, orient="horizontal").pack(fill="x", padx=14, pady=8)
        make_lbl(p, "Recurring Expenses", fg=ACCENT, font=FONT_B).pack()

        rec_form = tk.Frame(p, bg=BG)
        rec_form.pack(pady=4)
        make_lbl(rec_form, "Category:", bg=BG).grid(row=0, column=0, sticky="e", padx=6, pady=3)
        self.rec_cat = make_entry(rec_form, width=16)
        self.rec_cat.grid(row=0, column=1, pady=3)
        make_lbl(rec_form, "Amount ($):", bg=BG).grid(row=0, column=2, sticky="e", padx=6, pady=3)
        self.rec_amt = make_entry(rec_form, width=12)
        self.rec_amt.grid(row=0, column=3, pady=3)
        make_lbl(rec_form, "Every N days:", bg=BG).grid(row=0, column=4, sticky="e", padx=6, pady=3)
        self.rec_freq = make_entry(rec_form, width=8)
        self.rec_freq.grid(row=0, column=5, pady=3)

        rec_btn_row = tk.Frame(p, bg=BG)
        rec_btn_row.pack(pady=4)
        make_btn(rec_btn_row, "Add Recurring",
                 self._do_add_recurring).pack(side="left", padx=4)
        make_btn(rec_btn_row, "Delete Selected",
                 self._do_delete_recurring, RED).pack(side="left", padx=4)

        cols_r = ("Category", "Amount", "Every (days)", "Last Applied")
        widths_r = [180, 110, 120, 140]
        tfr, self.rec_tree = make_tree(p, cols_r, heights=4, col_widths=widths_r)
        tfr.pack(fill="x", padx=14, pady=(2, 10))

    def refresh_expense(self):
        for row in self.exp_tree.get_children():
            self.exp_tree.delete(row)
        for i, e in enumerate(self.dm.expenses, 1):
            rec = "✔" if e.get("recurring") else ""
            self.exp_tree.insert("", "end", values=(
                i, e.get("date", ""), e["category"],
                f"${e['amount']:.2f}", e.get("note", ""), rec))

        for row in self.rec_tree.get_children():
            self.rec_tree.delete(row)
        for r in self.dm.recurring:
            self.rec_tree.insert("", "end", values=(
                r["category"], f"${r['amount']:.2f}",
                int(r["frequency_days"]), r.get("last_added", "never")))

    def _do_add_expense(self):
        cat = self.exp_cat_combo.get().strip()
        if not cat or cat not in self.dm.categories:
            messagebox.showerror(
                "Error",
                "Select a valid category.\nCreate one in the Budget tab first.")
            return
        try:
            amt = float(self.exp_amt.get())
            if amt < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Enter a valid non-negative amount.")
            return
        note = self.exp_note.get().strip()
        self.dm.expenses.append({
            "category": cat,
            "amount":   amt,
            "date":     datetime.now().strftime("%Y-%m-%d"),
            "note":     note,
            "recurring": False,
        })
        self.exp_amt.delete(0, "end")
        self.exp_note.delete(0, "end")
        spent = self.dm.spent_in(cat)
        bud   = self.dm.categories[cat]
        pct   = spent / bud * 100 if bud > 0 else 0
        self.dm.maybe_save()
        self.refresh_all()
        if spent > bud:
            messagebox.showwarning(
                "Over Budget!",
                f"⚠ You've gone over budget in '{cat}'!\n"
                f"Budget: ${bud:.2f}  |  Spent: ${spent:.2f}")
        elif pct >= 80:
            messagebox.showwarning(
                "Caution",
                f"⚠ {pct:.1f}% of '{cat}' budget used.")

    def _do_edit_expense(self):
        sel = self.exp_tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Select an expense to edit.")
            return
        idx = self.exp_tree.index(sel[0])
        e   = self.dm.expenses[idx]

        dlg = tk.Toplevel(self)
        dlg.title("Edit Expense")
        dlg.configure(bg=BG)
        dlg.geometry("320x210")
        dlg.resizable(False, False)
        dlg.grab_set()

        make_lbl(dlg, "Edit Expense", fg=ACCENT, font=FONT_H).pack(pady=(16, 10))
        f = tk.Frame(dlg, bg=BG)
        f.pack()
        make_lbl(f, "Amount ($):", bg=BG).grid(row=0, column=0, sticky="e", padx=8, pady=5)
        amt_e = make_entry(f)
        amt_e.insert(0, str(e["amount"]))
        amt_e.grid(row=0, column=1, pady=5)
        make_lbl(f, "Note:", bg=BG).grid(row=1, column=0, sticky="e", padx=8, pady=5)
        note_e = make_entry(f, width=22)
        note_e.insert(0, e.get("note", ""))
        note_e.grid(row=1, column=1, pady=5)
        amt_e.focus()

        msg_l = make_lbl(dlg, "", fg=RED, font=FONT_S)
        msg_l.pack()

        def save():
            try:
                new_amt = float(amt_e.get())
                if new_amt < 0:
                    raise ValueError
                self.dm.expenses[idx]["amount"] = new_amt
                self.dm.expenses[idx]["note"]   = note_e.get().strip()
                self.dm.maybe_save()
                self.refresh_all()
                dlg.destroy()
            except ValueError:
                msg_l.config(text="Invalid amount.")

        make_btn(dlg, "Save Changes", save).pack(pady=8)

    def _do_delete_expense(self):
        sel = self.exp_tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Select an expense to delete.")
            return
        idx = self.exp_tree.index(sel[0])
        e   = self.dm.expenses[idx]
        if messagebox.askyesno(
                "Confirm Delete",
                f"Delete: {e['category']} — ${e['amount']:.2f}?"):
            self.dm.expenses.pop(idx)
            self.dm.maybe_save()
            self.refresh_all()

    def _do_add_recurring(self):
        cat = self.rec_cat.get().strip()
        if cat not in self.dm.categories:
            messagebox.showerror(
                "Error", "Category doesn't exist. Create it in the Budget tab.")
            return
        try:
            amt  = float(self.rec_amt.get());  assert amt > 0
            freq = float(self.rec_freq.get()); assert freq > 0
        except (ValueError, AssertionError):
            messagebox.showerror("Error", "Enter valid positive amount and frequency.")
            return
        self.dm.recurring.append({
            "category":      cat,
            "amount":        amt,
            "frequency_days": freq,
            "last_added":    datetime.now().strftime("%Y-%m-%d"),
        })
        self.rec_cat.delete(0, "end")
        self.rec_amt.delete(0, "end")
        self.rec_freq.delete(0, "end")
        self.dm.maybe_save()
        self.refresh_expense()

    def _do_delete_recurring(self):
        sel = self.rec_tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Select a recurring expense to delete.")
            return
        idx = self.rec_tree.index(sel[0])
        r   = self.dm.recurring[idx]
        if messagebox.askyesno(
                "Confirm Delete",
                f"Delete recurring: {r['category']} — ${r['amount']:.2f} / {int(r['frequency_days'])} day(s)?"):
            self.dm.recurring.pop(idx)
            self.dm.maybe_save()
            self.refresh_expense()

    #  TAB 4 — INCOME & SAVINGS

    def _build_income(self):
        p = self.tab_income
        make_lbl(p, "Income & Savings", fg=ACCENT, font=FONT_H).pack(pady=(16, 10))

        form = tk.Frame(p, bg=BG)
        form.pack()

        make_lbl(form, "Set total income ($):", bg=BG).grid(
            row=0, column=0, sticky="e", padx=8, pady=6)
        self.inc_set_e = make_entry(form)
        self.inc_set_e.grid(row=0, column=1, pady=6)
        make_lbl(form, "Note (opt):", bg=BG).grid(
            row=0, column=2, sticky="e", padx=8, pady=6)
        self.inc_set_note = make_entry(form, width=20)
        self.inc_set_note.grid(row=0, column=3, pady=6)
        make_btn(form, "Set Income", self._do_set_income, GREEN).grid(
            row=0, column=4, padx=8, pady=6)

        make_lbl(form, "Add to income ($):", bg=BG).grid(
            row=1, column=0, sticky="e", padx=8, pady=6)
        self.inc_add_e = make_entry(form)
        self.inc_add_e.grid(row=1, column=1, pady=6)
        make_lbl(form, "Note (opt):", bg=BG).grid(
            row=1, column=2, sticky="e", padx=8, pady=6)
        self.inc_add_note = make_entry(form, width=20)
        self.inc_add_note.grid(row=1, column=3, pady=6)
        make_btn(form, "Add Income", self._do_add_income, GREEN).grid(
            row=1, column=4, padx=8, pady=6)

        ttk.Separator(p, orient="horizontal").pack(fill="x", padx=14, pady=8)

        sav_row = tk.Frame(p, bg=BG)
        sav_row.pack()
        make_lbl(sav_row, "Savings goal ($):", bg=BG).pack(side="left", padx=8)
        self.sav_goal_e = make_entry(sav_row, width=18)
        self.sav_goal_e.pack(side="left", padx=6)
        make_btn(sav_row, "Set Goal", self._do_set_savings_goal).pack(side="left", padx=4)

        self.sav_info = make_lbl(p, "", fg=GREEN, font=FONT_S)
        self.sav_info.pack(pady=4)
        self.sav_bar = ttk.Progressbar(p, length=700, mode="determinate")
        self.sav_bar.pack(pady=4, padx=14)

        ttk.Separator(p, orient="horizontal").pack(fill="x", padx=14, pady=8)
        make_lbl(p, "Income History", fg=MUTED, font=FONT_S).pack(pady=(0, 2))
        cols = ("Date", "Action", "Amount", "Note")
        widths = [110, 90, 110, 360]
        tf, self.inc_tree = make_tree(p, cols, heights=9, col_widths=widths)
        tf.pack(fill="both", expand=True, padx=14, pady=(0, 10))

    def refresh_income(self):
        dm = self.dm
        if dm.savings_goal > 0:
            saved = max(0, dm.remaining())
            pct   = min(int(saved / dm.savings_goal * 100), 100)
            self.sav_bar["value"] = pct
            self.sav_goal_e.delete(0, "end")
            self.sav_goal_e.insert(0, str(dm.savings_goal))
            if pct >= 100:
                status, color = "🎉 Goal Reached!", GREEN
            elif dm.remaining() < 0:
                status, color = "⚠ Spending exceeds income!", RED
            else:
                status = f"${saved:.2f} / ${dm.savings_goal:.2f}  ({pct}%)"
                color  = YELLOW if pct >= 50 else FG
            self.sav_info.config(text=status, fg=color)
        else:
            self.sav_bar["value"] = 0
            self.sav_info.config(text="No savings goal set.", fg=MUTED)

        for row in self.inc_tree.get_children():
            self.inc_tree.delete(row)
        for entry in reversed(dm.income_history):
            action = "Set to" if entry["type"] == "set" else "Added"
            self.inc_tree.insert("", "end", values=(
                entry["date"], action,
                f"${entry['amount']:.2f}", entry.get("note", "")))

    def _do_set_income(self):
        try:
            amt = float(self.inc_set_e.get())
            assert amt >= 0
        except (ValueError, AssertionError):
            messagebox.showerror("Error", "Enter a valid non-negative amount.")
            return
        note = self.inc_set_note.get().strip()
        self.dm.income_history.append({
            "type": "set", "amount": amt,
            "date": datetime.now().strftime("%Y-%m-%d"), "note": note})
        self.dm.income = amt
        self.inc_set_e.delete(0, "end")
        self.inc_set_note.delete(0, "end")
        self.dm.maybe_save()
        self.refresh_all()

    def _do_add_income(self):
        try:
            amt = float(self.inc_add_e.get())
            assert amt > 0
        except (ValueError, AssertionError):
            messagebox.showerror("Error", "Enter a valid positive amount.")
            return
        note = self.inc_add_note.get().strip()
        self.dm.income += amt
        self.dm.income_history.append({
            "type": "add", "amount": amt,
            "date": datetime.now().strftime("%Y-%m-%d"), "note": note})
        self.inc_add_e.delete(0, "end")
        self.inc_add_note.delete(0, "end")
        self.dm.maybe_save()
        self.refresh_all()

    def _do_set_savings_goal(self):
        try:
            g = float(self.sav_goal_e.get())
            assert g >= 0
        except (ValueError, AssertionError):
            messagebox.showerror("Error", "Enter a valid non-negative amount.")
            return
        self.dm.savings_goal = g
        self.dm.maybe_save()
        self.refresh_income()
        self.refresh_dashboard()

    #  TAB 5 — REPORTS

    def _build_reports(self):
        p = self.tab_reports
        make_lbl(p, "Reports & Analytics", fg=ACCENT, font=FONT_H).pack(pady=(14, 8))

        # Monthly view
        month_row = tk.Frame(p, bg=BG)
        month_row.pack()
        make_lbl(month_row, "Month (YYYY-MM):", bg=BG).pack(side="left", padx=8)
        self.month_e = make_entry(month_row, width=12)
        self.month_e.pack(side="left", padx=4)
        make_btn(month_row, "Show Monthly", self._do_monthly_view).pack(side="left", padx=4)

        self.monthly_lbl = make_lbl(p, "", fg=GREEN, font=FONT_S)
        self.monthly_lbl.pack(pady=2)
        cols_m = ("Date", "Category", "Amount", "Note")
        widths_m = [100, 160, 100, 320]
        tfm, self.monthly_tree = make_tree(p, cols_m, heights=4, col_widths=widths_m)
        tfm.pack(fill="x", padx=14, pady=(0, 4))

        # Search
        ttk.Separator(p, orient="horizontal").pack(fill="x", padx=14, pady=6)
        search_top = tk.Frame(p, bg=BG)
        search_top.pack()
        make_lbl(search_top, "Search by:", bg=BG).pack(side="left", padx=8)
        self.search_mode = ttk.Combobox(
            search_top,
            values=["Category", "Date Range", "Amount Range"],
            width=14, font=FONT, state="readonly")
        self.search_mode.current(0)
        self.search_mode.pack(side="left", padx=4)
        make_lbl(search_top, "Q1:", bg=BG).pack(side="left")
        self.search_q1 = make_entry(search_top, width=14)
        self.search_q1.pack(side="left", padx=4)
        make_lbl(search_top, "Q2:", bg=BG).pack(side="left")
        self.search_q2 = make_entry(search_top, width=14)
        self.search_q2.pack(side="left", padx=4)
        make_btn(search_top, "Search", self._do_search).pack(side="left", padx=4)

        make_lbl(p,
                 "Category → Q1: name     |     Date Range → Q1: start, Q2: end (YYYY-MM-DD)"
                 "     |     Amount Range → Q1: min, Q2: max",
                 fg=MUTED, font=("Segoe UI", 8)).pack()

        self.search_lbl = make_lbl(p, "", fg=MUTED, font=FONT_S)
        self.search_lbl.pack(pady=2)
        cols_s = ("Date", "Category", "Amount", "Note")
        widths_s = [100, 160, 100, 320]
        tfs, self.search_tree = make_tree(p, cols_s, heights=4, col_widths=widths_s)
        tfs.pack(fill="x", padx=14)

        # Charts & Export
        ttk.Separator(p, orient="horizontal").pack(fill="x", padx=14, pady=8)
        btn_row = tk.Frame(p, bg=BG)
        btn_row.pack(pady=4)
        make_btn(btn_row, "📊 Budget vs Spent",
                 self._plot_bar,   ACCENT).pack(side="left", padx=6)
        make_btn(btn_row, "📈 Monthly Trend",
                 self._plot_trend, ACCENT).pack(side="left", padx=6)
        make_btn(btn_row, "🍕 Spending Pie",
                 self._plot_pie,   ACCENT).pack(side="left", padx=6)
        make_btn(btn_row, "📁 Export CSV",
                 self._export_csv, GREEN).pack(side="left", padx=6)

        if not MATPLOTLIB_AVAILABLE:
            make_lbl(p,
                     "Charts require matplotlib — install with: pip install matplotlib",
                     fg=RED, font=FONT_S).pack(pady=4)

    def _do_monthly_view(self):
        month = self.month_e.get().strip()
        try:
            datetime.strptime(month + "-01", "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Use format YYYY-MM  (e.g. 2025-03)")
            return
        filtered = [e for e in self.dm.expenses if e["date"].startswith(month)]
        for row in self.monthly_tree.get_children():
            self.monthly_tree.delete(row)
        total = 0
        for e in filtered:
            self.monthly_tree.insert("", "end", values=(
                e["date"], e["category"],
                f"${e['amount']:.2f}", e.get("note", "")))
            total += e["amount"]
        if filtered:
            self.monthly_lbl.config(
                text=f"Total for {month}: ${total:.2f}  ({len(filtered)} expenses)",
                fg=GREEN)
        else:
            self.monthly_lbl.config(text=f"No expenses found for {month}.", fg=MUTED)

    def _do_search(self):
        mode = self.search_mode.get()
        q1   = self.search_q1.get().strip()
        q2   = self.search_q2.get().strip()
        results = []

        if mode == "Category":
            results = [e for e in self.dm.expenses if e["category"] == q1]
        elif mode == "Date Range":
            try:
                datetime.strptime(q1, "%Y-%m-%d")
                datetime.strptime(q2, "%Y-%m-%d")
                results = [e for e in self.dm.expenses if q1 <= e["date"] <= q2]
            except ValueError:
                messagebox.showerror("Error", "Use YYYY-MM-DD for both dates.")
                return
        elif mode == "Amount Range":
            try:
                mn = float(q1)
                mx = float(q2) if q2 else float("inf")
                results = [e for e in self.dm.expenses if mn <= e["amount"] <= mx]
            except ValueError:
                messagebox.showerror("Error", "Enter valid numbers.")
                return

        for row in self.search_tree.get_children():
            self.search_tree.delete(row)
        total = 0
        for e in results:
            self.search_tree.insert("", "end", values=(
                e["date"], e["category"],
                f"${e['amount']:.2f}", e.get("note", "")))
            total += e["amount"]
        if results:
            self.search_lbl.config(
                text=f"{len(results)} result(s)  |  Total: ${total:.2f}", fg=GREEN)
        else:
            self.search_lbl.config(text="No results found.", fg=MUTED)

    def _plot_bar(self):
        if not MATPLOTLIB_AVAILABLE:
            messagebox.showerror("Error", "Install matplotlib: pip install matplotlib")
            return
        if not self.dm.categories:
            messagebox.showinfo("Info", "No categories to plot.")
            return
        cats    = list(self.dm.categories.keys())
        budgets = [self.dm.categories[c] for c in cats]
        spent   = [self.dm.spent_in(c) for c in cats]
        x = range(len(cats)); w = 0.35
        fig, ax = plt.subplots(figsize=(10, 5))
        fig.patch.set_facecolor("#1e1e2e")
        ax.set_facecolor("#2a2a3e")
        ax.bar([i - w/2 for i in x], budgets, w, color="#7c6af7", label="Budget", alpha=0.85)
        ax.bar([i + w/2 for i in x], spent,   w, color="#4caf82", label="Spent",  alpha=0.85)
        ax.set_xticks(list(x))
        ax.set_xticklabels(cats, rotation=30, ha="right", color=FG)
        ax.set_ylabel("Amount ($)", color=FG)
        ax.set_title(f"Budget vs Spent — v{VERSION}", color=FG)
        ax.tick_params(colors=FG)
        ax.legend(facecolor=PANEL, labelcolor=FG)
        ax.spines[:].set_color(MUTED)
        fig.tight_layout()
        plt.show()

    def _plot_trend(self):
        if not MATPLOTLIB_AVAILABLE:
            messagebox.showerror("Error", "Install matplotlib: pip install matplotlib")
            return
        if not self.dm.expenses:
            messagebox.showinfo("Info", "No expenses to plot.")
            return
        totals = {}
        for e in self.dm.expenses:
            m = e["date"][:7]
            totals[m] = totals.get(m, 0) + e["amount"]
        months = sorted(totals.keys())
        fig, ax = plt.subplots(figsize=(10, 5))
        fig.patch.set_facecolor("#1e1e2e")
        ax.set_facecolor("#2a2a3e")
        ax.plot(months, [totals[m] for m in months],
                marker="o", lw=2, color="#7c6af7", markersize=8)
        ax.set_xlabel("Month", color=FG)
        ax.set_ylabel("Total ($)", color=FG)
        ax.set_title(f"Monthly Expense Trend — v{VERSION}", color=FG)
        ax.tick_params(axis="x", rotation=30, colors=FG)
        ax.tick_params(axis="y", colors=FG)
        ax.grid(True, alpha=0.2, color=MUTED)
        ax.spines[:].set_color(MUTED)
        fig.tight_layout()
        plt.show()

    def _plot_pie(self):
        if not MATPLOTLIB_AVAILABLE:
            messagebox.showerror("Error", "Install matplotlib: pip install matplotlib")
            return
        if not self.dm.expenses:
            messagebox.showinfo("Info", "No expenses to plot.")
            return
        totals = {}
        for e in self.dm.expenses:
            totals[e["category"]] = totals.get(e["category"], 0) + e["amount"]
        fig, ax = plt.subplots(figsize=(8, 6))
        fig.patch.set_facecolor("#1e1e2e")
        ax.pie(list(totals.values()), labels=list(totals.keys()),
               autopct="%1.1f%%", startangle=140,
               textprops={"color": FG})
        ax.set_title(f"Spending by Category — v{VERSION}", color=FG)
        fig.tight_layout()
        plt.show()

    def _export_csv(self):
        if not self.dm.expenses:
            messagebox.showinfo("Info", "No expenses to export.")
            return
        ts   = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        path = os.path.join(DATA_DIR, f"expenses_export_{ts}.csv")
        try:
            with open(path, "w", newline="") as f:
                w = csv.DictWriter(
                    f, fieldnames=["date", "category", "amount", "note", "recurring"])
                w.writeheader()
                for e in self.dm.expenses:
                    w.writerow({
                        "date":      e.get("date", ""),
                        "category":  e.get("category", ""),
                        "amount":    e.get("amount", 0),
                        "note":      e.get("note", ""),
                        "recurring": e.get("recurring", False),
                    })
            messagebox.showinfo("Exported", f"CSV saved to:\n{path}")
        except Exception as ex:
            messagebox.showerror("Export Error", str(ex))

    #  TAB 6 — SETTINGS

    def _build_settings(self):
        p = self.tab_settings
        make_lbl(p, "Settings", fg=ACCENT, font=FONT_H).pack(pady=(16, 12))

        # Data management group
        grp = tk.LabelFrame(p, text=" Data Management ", bg=BG, fg=MUTED,
                             font=FONT_S, bd=1, relief="groove")
        grp.pack(fill="x", padx=30, pady=6)
        btn_row = tk.Frame(grp, bg=BG)
        btn_row.pack(pady=12)
        make_btn(btn_row, "💾  Save Data",
                 self._settings_save).pack(side="left", padx=8)
        make_btn(btn_row, "📂  Load Data",
                 self._settings_load).pack(side="left", padx=8)
        make_btn(btn_row, "🔄  Restore Backup",
                 self._settings_restore, YELLOW).pack(side="left", padx=8)
        self.autosave_btn = make_btn(btn_row, "", self._toggle_autosave)
        self.autosave_btn.pack(side="left", padx=8)

        make_lbl(p, f"Data folder: {DATA_DIR}", fg=MUTED, font=FONT_S).pack(pady=4)

        ttk.Separator(p, orient="horizontal").pack(fill="x", padx=30, pady=10)

        # Security group
        grp2 = tk.LabelFrame(p, text=" Security ", bg=BG, fg=MUTED,
                              font=FONT_S, bd=1, relief="groove")
        grp2.pack(fill="x", padx=30, pady=6)
        make_btn(grp2, "🔑  Change Password",
                 self._change_password).pack(pady=12)

        ttk.Separator(p, orient="horizontal").pack(fill="x", padx=30, pady=10)

        # About group
        grp3 = tk.LabelFrame(p, text=" About ", bg=BG, fg=MUTED,
                              font=FONT_S, bd=1, relief="groove")
        grp3.pack(fill="x", padx=30, pady=6)
        make_lbl(grp3, f"Budget Tracker  v{VERSION}",
                 fg=ACCENT, font=FONT_B).pack(pady=(10, 2))
        make_lbl(grp3, "Built with Python & Tkinter", fg=MUTED, font=FONT_S).pack()
        make_lbl(grp3, "Data stored in ~/BudgetTrackerData/",
                 fg=MUTED, font=FONT_S).pack(pady=(0, 10))

        self._update_autosave_btn()

    def _update_autosave_btn(self):
        state = "ON" if self.dm.autosave else "OFF"
        color = GREEN if self.dm.autosave else MUTED
        self.autosave_btn.config(text=f"Auto-Save: {state}", bg=color)

    def _toggle_autosave(self):
        self.dm.autosave = not self.dm.autosave
        self._update_autosave_btn()
        self.dm.maybe_save()

    def _settings_save(self):
        self.dm.save()

    def _settings_load(self):
        if messagebox.askyesno("Load Data", "Reload from disk? Unsaved changes will be lost."):
            self.dm.load()
            self.refresh_all()

    def _settings_restore(self):
        if messagebox.askyesno(
                "Restore Backup",
                "Restore from last backup?\nCurrent unsaved data will be overwritten."):
            if self.dm.restore_backup():
                messagebox.showinfo("Restored", "Backup restored successfully.")
                self.refresh_all()
            else:
                messagebox.showerror("Error", "No backup file found.")

    def _change_password(self):
        dlg = tk.Toplevel(self)
        dlg.title("Change Password")
        dlg.configure(bg=BG)
        dlg.geometry("340x270")
        dlg.resizable(False, False)
        dlg.grab_set()

        make_lbl(dlg, "Change Password", fg=ACCENT, font=FONT_H).pack(pady=(16, 10))
        f = tk.Frame(dlg, bg=BG)
        f.pack()

        make_lbl(f, "Current password:", bg=BG).grid(row=0, column=0, sticky="e", padx=8, pady=5)
        cur_e = make_entry(f, show="*")
        cur_e.grid(row=0, column=1, pady=5)

        make_lbl(f, "New password:", bg=BG).grid(row=1, column=0, sticky="e", padx=8, pady=5)
        new_e = make_entry(f, show="*")
        new_e.grid(row=1, column=1, pady=5)

        make_lbl(f, "Confirm new:", bg=BG).grid(row=2, column=0, sticky="e", padx=8, pady=5)
        cnf_e = make_entry(f, show="*")
        cnf_e.grid(row=2, column=1, pady=5)

        make_lbl(f, "New hint (opt):", bg=BG).grid(row=3, column=0, sticky="e", padx=8, pady=5)
        hint_e = make_entry(f)
        hint_e.grid(row=3, column=1, pady=5)

        cur_e.focus()
        msg_l = make_lbl(dlg, "", fg=RED, font=FONT_S)
        msg_l.pack(pady=2)

        def do_change():
            if not self.pm.check(cur_e.get()):
                msg_l.config(text="Wrong current password.")
                return
            pw1 = new_e.get()
            pw2 = cnf_e.get()
            if len(pw1) < 4:
                msg_l.config(text="Minimum 4 characters.")
                return
            if pw1 != pw2:
                msg_l.config(text="Passwords do not match.")
                return
            self.pm.set(pw1)
            self.pm.set_hint(hint_e.get().strip())
            dlg.destroy()
            messagebox.showinfo("Success", "Password changed successfully.")

        make_btn(dlg, "Change Password", do_change).pack(pady=6)

    #  TAB 7 — HELP

    def _build_help(self):
        p = self.tab_help
        make_lbl(p, "Help & User Guide", fg=ACCENT, font=FONT_H).pack(pady=(16, 10))

        frame = tk.Frame(p, bg=BG)
        frame.pack(fill="both", expand=True, padx=16, pady=(0, 14))
        sb = tk.Scrollbar(frame)
        sb.pack(side="right", fill="y")
        txt = tk.Text(frame, bg=PANEL, fg=FG, font=("Consolas", 10),
                      relief="flat", wrap="word", padx=14, pady=10,
                      yscrollcommand=sb.set, highlightthickness=0)
        txt.pack(fill="both", expand=True)
        sb.config(command=txt.yview)

        guide = f"""\
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Budget Tracker  v{VERSION}  —  User Guide
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GETTING STARTED
───────────────
1. On first launch, create a password (minimum 4 characters).
   You can also add a hint that appears on the login screen.
2. Go to Income & Savings and set your total income.
3. Go to Budget and create spending categories (e.g. Food, Transport).
4. Log your expenses in the Expenses tab.
5. Monitor everything on the Dashboard.


DASHBOARD TAB
─────────────
• Shows Income, Total Spent, Remaining balance, and Financial Health.

  Health status:
    Healthy       — spending below 60% of income      (green)
    Caution       — 60–90% of income spent            (yellow)
    Overspending  — over 90% of income spent          (red)

• Savings Goal progress bar tracks how close you are to your goal.
• Category Overview lists every category's budget, spending, and usage.
  Rows turn yellow at 80% usage and red when over budget.


BUDGET TAB
──────────
• Enter a category name and amount, then click "Set / Update Budget".
• Entering an existing category name updates its budget amount.
• Click "Edit Selected" to pre-fill the form with a selected category.
• Click "Delete Selected" to remove a category and ALL its expenses.
  (Confirmation required — this cannot be undone.)
• A warning appears if the total of all budgets exceeds your income,
  but you may choose to continue anyway.


EXPENSES TAB
────────────
• Pick a category from the dropdown (populated from your Budget tab).
• Enter the amount and an optional note, then click "Add Expense".
• Warnings appear when you reach 80% or exceed a category's budget.
• "Edit Selected" opens a dialog to change the amount or note.
• "Delete Selected" removes the selected expense (confirmation required).
• The "Rec?" column shows ✔ for automatically applied recurring expenses.

RECURRING EXPENSES (lower section):
• Enter a category name, amount, and frequency in days.
• Click "Add Recurring" to save it.
• Each time the app launches, it checks if any recurring expense is due
  (based on last-applied date + frequency) and applies it automatically.
• A notification appears if any were applied at startup.
• Delete a recurring entry by selecting it and clicking "Delete Selected".


INCOME & SAVINGS TAB
────────────────────
• "Set total income"  — replaces your income with a new value.
• "Add to income"     — adds on top of your existing income
                        (useful for extra earnings or bonuses).
• Both actions are logged in the Income History table below.
• Set a Savings Goal amount to track your savings progress.
• The progress bar fills as your remaining balance approaches the goal.
• A 🎉 message appears when you reach or exceed the goal.


REPORTS TAB
───────────
Monthly View:
  Enter a month in YYYY-MM format (e.g. 2025-03) and click "Show Monthly"
  to see all expenses for that month with a running total.

Search:
  Category     — Q1: exact category name
  Date Range   — Q1: start date, Q2: end date  (YYYY-MM-DD)
  Amount Range — Q1: minimum, Q2: maximum (leave Q2 blank for no limit)
  Results are shown below with a count and total.

Charts (requires matplotlib — pip install matplotlib):
  📊 Budget vs Spent  — grouped bar chart per category
  📈 Monthly Trend    — line chart of total monthly expenses over time
  🍕 Spending Pie     — proportion of spending per category

Export CSV:
  Saves all expenses to a timestamped .csv file in ~/BudgetTrackerData/.
  Useful for external analysis in Excel or Google Sheets.


SETTINGS TAB
────────────
• 💾 Save Data      — manually saves all data to disk.
• 📂 Load Data      — reloads data from disk (prompts for confirmation).
• 🔄 Restore Backup — restores the most recent automatic backup.
• Auto-Save (green = ON) — when enabled, data is saved after every change.
  Turn OFF if you prefer to save manually.
• 🔑 Change Password — enter your current password, then set a new one.
  Optionally update your hint as well.


SECURITY & DATA
───────────────
• Passwords are stored as SHA-256 hashes, never in plain text.
• Data file: ~/BudgetTrackerData/budget_data.json
• Up to 5 automatic timestamped backups are kept in the same folder.
• "Restore Backup" recovers the last backup saved before the current file.
• If you forget your password: click "Forgot password?" on the login screen.
  CAUTION — this permanently deletes ALL data to reset the app.


TIPS
────
• Category names are case-sensitive: "food" ≠ "Food"!
• You cannot log an expense under a category that doesn't exist yet.
• Use notes to keep track of what each expense was for.
• Keep Auto-Save ON to avoid accidental data loss.
• Export to CSV regularly for external backups.
• Recurring expenses are only applied once per app launch per due date.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Budget Tracker v{VERSION} !
  Built with Python & Tk Interface Library
  Data stored in: ~/BudgetTrackerData/ (Folder)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        txt.insert("1.0", guide)
        txt.config(state="disabled")

    #  GLOBAL REFRESH

    def refresh_all(self):
        self.refresh_dashboard()
        self.refresh_budget()
        self.refresh_expense()
        self.refresh_income()
        self._update_autosave_btn()


#  ENTRY POINT

if __name__ == "__main__":
    app = BudgetApp()
    app.mainloop()