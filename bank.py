import tkinter as tk
import re
from tkinter import messagebox

valid_users = {"user1": "password1", "user2": "password2", "user3": "password3" ,"user4": "password4"}

class BankAccount:
    def __init__(self, account_num, acc_holder, balance=0.0):
        self.account_num = account_num
        self.acc_holder = acc_holder
        self.balance = balance
        self.transaction_history = []
    
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transaction_history.append(f"Deposited: Rs.{amount}")
            messagebox.showinfo(f"Transaction Successful!", f"Deposited Rs.{amount}. New balance: Rs.{self.balance}.")
        else:
            messagebox.showinfo("ERROR!", f"Deposit amount must be positive. Please enter an appropriate value.")

    def withdraw(self, amount):
        if self.balance > amount:
            self.balance -= amount
            self.transaction_history.append(f"Withdrawn: Rs.{amount}")
            messagebox.showinfo("Transaction Successful!", f"Withdrawn Rs.{amount}. New Balance: {self.balance}.")
        elif amount > self.balance:
            messagebox.showinfo("ERROR!", "Insufficient Funds. Please change amount to be withdrawn.")
        else:
            messagebox.showinfo("ERROR!", "Invalid value. Amount to be withdrawn must be positive. Please enter an appropriate value.")
    def transfer(self,amount,target_account):
        if self.account_num!= target_account.account_num:
            if self.balance<amount:
                messagebox.showerror("ERROR!","Insufficient funds. Please try later")
            else:
                self.balance-=amount
                target_account.balance+=amount
                self.transaction_history.append(f"Transferrd: Rs.{amount} To: {target_account.acc_holder}")
                target_account.transaction_history.append(f"Recieved: Rs{amount} From: {self.acc_holder}")
                messagebox.showinfo("Transaction Successful!",f"Transferrd: Rs.{amount} To: {target_account.acc_holder}")
        else:
            messagebox.showerror("ERROR!","Please enter an appropriate account number!")
  
class SavingsAccount(BankAccount):
    def __init__(self, account_num, acc_holder, balance=0.0, interest_rate=0.02):
        super().__init__(account_num, acc_holder, balance)
        self.interest_rate = interest_rate

    def add_interest(self):
        interest = self.balance * self.interest_rate
        self.balance += interest
        messagebox.showinfo(f"Transaction Successful!", f"Added interest: {interest}. New balance: {self.balance}")


class CurrentAccount(BankAccount):
    def __init__(self, account_num, acc_holder, balance=0.0, overdraft_limit=1000):
        super().__init__(account_num, acc_holder, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if 0 < amount <= self.balance + self.overdraft_limit:
            self.balance -= amount
            self.transaction_history.append(f"Withdrawn: Rs.{amount}")
            messagebox.showinfo("Transaction Successful!", f"Withdrawn Rs.{amount}. New balance: Rs.{self.balance}")
        else:
            messagebox.showinfo("ERROR!", "Withdrawal exceeds overdraft limit or is invalid.")
    

class BankingSystem:
    def __init__(self, root):
        self.amt = 0.0
        self.root = root
        self.root.title("Banking System")
        self.current_user = None
        self.accounts = {
            "user1": SavingsAccount("001", "Rohit", 5000, 0.05),
            "user2": SavingsAccount("002", "Aishwariya", 6000, 0.09),
            "user3": CurrentAccount("003", "Nikhil", 4500, 1000),
            "user4": CurrentAccount("004", "Kiara", 5000, 1500)
        }
        self.account_ids={"001":"user1","002":"user2","003":"user3","004":"user4"}
        self.create_login_page()

    def create_login_page(self):
        self.clear_window()
        self.root.configure(bg='#CBBFDD') 

        tk.Label(self.root, text="Welcome to RSB!", font=("Times New Roman", 25, "bold"), bg="purple",fg="white").pack(pady=20)
        tk.Label(self.root, text="Banking made so easy, even your dog could do it!", font=("georgia", 18), fg="purple").pack(pady=5)

        tk.Label(self.root, text="User ID:", font=("Arial", 12)).pack(pady=5)
        self.user_id_entry = tk.Entry(self.root, font=("Arial", 14))
        self.user_id_entry.pack(pady=10, ipady=5)

        tk.Label(self.root, text="Password:", font=("Arial", 12)).pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*", font=("Arial", 14))
        self.password_entry.pack(pady=10, ipady=5)

        tk.Button(self.root, text="Login", command=self.verify_login, font=("Arial", 14), bg="#786B89",fg="white").pack(pady=20)

    def verify_login(self):
        user_id = self.user_id_entry.get()
        password = self.password_entry.get()

        if valid_users.get(user_id) == password:
            self.current_user = self.accounts[user_id]
            messagebox.showinfo("Welcome!", f"Hello, {self.current_user.acc_holder}!")
            self.choose_actions()
        else:
            messagebox.showerror("Login Failed", "Invalid User ID or Password")

    def choose_actions(self):
        self.clear_window()
        self.root.title("Account Actions")

        self.display_label = tk.Label(self.root, text=f"Account Holder: {self.current_user.acc_holder}\nAccount Number: {self.current_user.account_num}\n Account Type: {self.current_user.__class__.__name__}", font=("Times New Roman", 20), bg="#837ab6", padx=100, pady=50)
        self.display_label.pack()

        self.display_info = tk.Label(self.root, text="What would you like to do?", font=("Helvetica", 16), bg="#9d85b6")
        self.display_info.pack(pady=10)

        tk.Button(self.root, text="Deposit", command=self.deposit, font=("Arial", 14), bg="#E37DAC").pack(pady=10, fill="x", padx=100)
        tk.Button(self.root, text="Withdraw", command=self.withdraw, font=("Arial", 14), bg="#E37DAC").pack(pady=10, fill="x", padx=100)
        tk.Button(self.root, text="Transfer Money", command=self.transfer_money, font=("Arial", 14), bg="#E37DAC").pack(pady=10, fill="x", padx=100)
        tk.Button(self.root, text="Transaction History", command=self.transact_history, font=("Arial", 14), bg="#E37DAC").pack(pady=10, fill="x", padx=100)
        tk.Button(self.root, text="Check Balance", command=self.check_bal, font=("Arial", 14), bg="#E37DAC").pack(pady=10, fill="x", padx=100)
        tk.Button(self.root, text="Logout", command=self.logout, font=("Arial", 14), bg="#B05994").pack(pady=20)

    def deposit(self):
        def check_amount():
            amt = self.deposit_entry.get()
            if re.search(r"[^\d.]", amt):
                messagebox.showerror("ERROR!", "Please enter a valid amount")
            else:
                try:
                    amount = float(amt)
                    self.current_user.deposit(amount)
                except ValueError:
                    messagebox.showerror("ERROR!", "Invalid amount entered. Please try again.")
        self.clear_window()
        self.root.configure(bg='#CBBFDD') 
        self.display_info = tk.Label(self.root, text="Enter amount to deposit:", font=("Times New Roman", 16)).pack(pady=10)
        self.deposit_entry = tk.Entry(self.root, font=("Arial", 14))
        self.deposit_entry.pack(pady=10, ipady=5)
        self.submit_button = tk.Button(self.root, text="Submit", command=check_amount, font=("Arial", 14), bg="lightgreen")
        self.submit_button.pack(pady=10)
        self.back_button = tk.Button(self.root, text="Back", command=self.choose_actions, font=("Arial", 14), bg="#B05994")
        self.back_button.pack(pady=10)

    def withdraw(self):
        def check_amount():
            amt = self.withdraw_entry.get()
            if re.search(r"[^\d.]", amt):
                messagebox.showerror("ERROR!", "Please enter a valid amount")
            else:
                try:
                    amount = float(amt)
                    self.current_user.withdraw(amount)
                except ValueError:
                    messagebox.showerror("ERROR!", "Invalid amount entered. Please try again.")
        self.clear_window()
        root.configure(bg='#CBBFDD') 
        self.display_info = tk.Label(self.root, text="Enter amount to withdraw:", font=("times New Roman", 16)).pack(pady=50)
        self.withdraw_entry = tk.Entry(self.root, font=("Arial", 14))
        self.withdraw_entry.pack(pady=10, ipady=5)
        self.submit_button = tk.Button(self.root, text="Submit", command=check_amount, font=("Arial", 14), bg="lightgreen")
        self.submit_button.pack(pady=10)
        self.back_button = tk.Button(self.root, text="Back", command=self.choose_actions, font=("Arial", 14), bg="#B05994")
        self.back_button.pack(pady=10)
    def transfer_money(self):
        def check_amount():
            amt = self.trans_entry.get()
            acc= self.trans_acc.get()
            acc_id=self.account_ids.get(acc)
            if re.search(r"[^\d.]", amt):
                messagebox.showerror("ERROR!", "Please enter a valid amount")
            else:
                try:
                    amount = float(amt)
                    self.current_user.transfer(amount, self.accounts[acc_id])
                except ValueError:
                    messagebox.showerror("ERROR!", "Invalid amount entered. Please try again.")
        self.clear_window()
        root.configure(bg='#CBBFDD') 
        self.display_info = tk.Label(self.root, text="Enter amount to Transfer:", font=("times New Roman", 16)).pack(pady=50)
        self.trans_entry = tk.Entry(self.root, font=("Arial", 14))
        self.trans_entry.pack(pady=10, ipady=5)
        self.display_acc = tk.Label(self.root, text="Enter account number to transfer to:", font=("times New Roman", 16)).pack(pady=50)
        self.trans_acc = tk.Entry(self.root, font=("Arial", 14))
        self.trans_acc.pack(pady=10, ipady=5)
        self.submit_button = tk.Button(self.root, text="Submit", command=check_amount, font=("Arial", 14), bg="lightgreen")
        self.submit_button.pack(pady=10)
        self.back_button = tk.Button(self.root, text="Back", command=self.choose_actions, font=("Arial", 14), bg="#B05994")
        self.back_button.pack(pady=10)

    def transact_history(self):
        if self.current_user.transaction_history:
            transactions = "\n".join(self.current_user.transaction_history)
            self.display_info.config(text=f"Transaction History:\n{transactions}")
        else:
            self.display_info.config(text="No transaction history available.")

    def check_bal(self):
        self.display_info.config(text=f"Current Balance: Rs.{self.current_user.balance}")

    def logout(self):
        self.current_user = None
        self.create_login_page()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

root = tk.Tk()
root.geometry("550x550")
BankingSystem(root)
root.mainloop()
