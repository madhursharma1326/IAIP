import tkinter as tk
from tkinter import messagebox
from datetime import datetime


class BankingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Online Banking System")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        self.users = {
            "admin": {
                "password": "1234",
                "balance": 1000.0,
                "transactions": []
            }
        }

        self.current_user = None
        self.login_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Online Banking Login", font=("Arial", 24, "bold")).pack(pady=30)

        tk.Label(self.root, text="Username", font=("Arial", 12)).pack()
        self.username_entry = tk.Entry(self.root, font=("Arial", 12))
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text="Password", font=("Arial", 12)).pack()
        self.password_entry = tk.Entry(self.root, font=("Arial", 12), show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self.root, text="Login", width=20, command=self.login).pack(pady=15)
        tk.Button(self.root, text="Create Account", width=20, command=self.create_account_screen).pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in self.users and self.users[username]["password"] == password:
            self.current_user = username
            messagebox.showinfo("Success", "Login successful!")
            self.dashboard()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def create_account_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Create New Account", font=("Arial", 24, "bold")).pack(pady=30)

        tk.Label(self.root, text="Username", font=("Arial", 12)).pack()
        self.new_username_entry = tk.Entry(self.root, font=("Arial", 12))
        self.new_username_entry.pack(pady=5)

        tk.Label(self.root, text="Password", font=("Arial", 12)).pack()
        self.new_password_entry = tk.Entry(self.root, font=("Arial", 12), show="*")
        self.new_password_entry.pack(pady=5)

        tk.Label(self.root, text="Initial Deposit", font=("Arial", 12)).pack()
        self.initial_deposit_entry = tk.Entry(self.root, font=("Arial", 12))
        self.initial_deposit_entry.pack(pady=5)

        tk.Button(self.root, text="Create Account", width=20, command=self.create_account).pack(pady=15)
        tk.Button(self.root, text="Back to Login", width=20, command=self.login_screen).pack()

    def create_account(self):
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()
        initial_deposit = self.initial_deposit_entry.get()

        if username == "" or password == "":
            messagebox.showerror("Error", "Username and password cannot be empty")
            return

        if username in self.users:
            messagebox.showerror("Error", "Username already exists")
            return

        try:
            initial_deposit = float(initial_deposit)
            if initial_deposit < 0:
                messagebox.showerror("Error", "Initial deposit cannot be negative")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid deposit amount")
            return

        self.users[username] = {
            "password": password,
            "balance": initial_deposit,
            "transactions": [
                f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Account created with ${initial_deposit:.2f}"
            ]
        }

        messagebox.showinfo("Success", "Account created successfully!")
        self.login_screen()

    def dashboard(self):
        self.clear_screen()

        tk.Label(
            self.root,
            text=f"Welcome, {self.current_user}",
            font=("Arial", 22, "bold")
        ).pack(pady=20)

        tk.Button(self.root, text="Check Balance", width=25, command=self.check_balance).pack(pady=8)
        tk.Button(self.root, text="Deposit Money", width=25, command=self.deposit_screen).pack(pady=8)
        tk.Button(self.root, text="Withdraw Money", width=25, command=self.withdraw_screen).pack(pady=8)
        tk.Button(self.root, text="Transaction History", width=25, command=self.transaction_history).pack(pady=8)
        tk.Button(self.root, text="Logout", width=25, command=self.logout).pack(pady=20)

    def check_balance(self):
        balance = self.users[self.current_user]["balance"]
        messagebox.showinfo("Balance", f"Your current balance is: ${balance:.2f}")

    def deposit_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Deposit Money", font=("Arial", 24, "bold")).pack(pady=30)

        tk.Label(self.root, text="Enter amount", font=("Arial", 12)).pack()
        self.deposit_entry = tk.Entry(self.root, font=("Arial", 12))
        self.deposit_entry.pack(pady=10)

        tk.Button(self.root, text="Deposit", width=20, command=self.deposit_money).pack(pady=10)
        tk.Button(self.root, text="Back", width=20, command=self.dashboard).pack()

    def deposit_money(self):
        try:
            amount = float(self.deposit_entry.get())

            if amount <= 0:
                messagebox.showerror("Error", "Deposit amount must be greater than zero")
                return

            self.users[self.current_user]["balance"] += amount
            self.add_transaction(f"Deposited ${amount:.2f}")

            messagebox.showinfo("Success", f"${amount:.2f} deposited successfully")
            self.dashboard()

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")

    def withdraw_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="Withdraw Money", font=("Arial", 24, "bold")).pack(pady=30)

        tk.Label(self.root, text="Enter amount", font=("Arial", 12)).pack()
        self.withdraw_entry = tk.Entry(self.root, font=("Arial", 12))
        self.withdraw_entry.pack(pady=10)

        tk.Button(self.root, text="Withdraw", width=20, command=self.withdraw_money).pack(pady=10)
        tk.Button(self.root, text="Back", width=20, command=self.dashboard).pack()

    def withdraw_money(self):
        try:
            amount = float(self.withdraw_entry.get())

            if amount <= 0:
                messagebox.showerror("Error", "Withdrawal amount must be greater than zero")
                return

            if amount > self.users[self.current_user]["balance"]:
                messagebox.showerror("Error", "Insufficient funds")
                return

            self.users[self.current_user]["balance"] -= amount
            self.add_transaction(f"Withdrew ${amount:.2f}")

            messagebox.showinfo("Success", f"${amount:.2f} withdrawn successfully")
            self.dashboard()

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")

    def transaction_history(self):
        self.clear_screen()
        tk.Label(self.root, text="Transaction History", font=("Arial", 22, "bold")).pack(pady=20)

        history_box = tk.Text(self.root, width=65, height=18, font=("Arial", 10))
        history_box.pack(pady=10)

        transactions = self.users[self.current_user]["transactions"]

        if not transactions:
            history_box.insert(tk.END, "No transactions found.")
        else:
            for transaction in transactions:
                history_box.insert(tk.END, transaction + "\n")

        history_box.config(state=tk.DISABLED)

        tk.Button(self.root, text="Back", width=20, command=self.dashboard).pack(pady=10)

    def add_transaction(self, description):
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.users[self.current_user]["transactions"].append(f"{time} - {description}")

    def logout(self):
        self.current_user = None
        messagebox.showinfo("Logout", "Logged out successfully")
        self.login_screen()


root = tk.Tk()
app = BankingSystem(root)
root.mainloop()