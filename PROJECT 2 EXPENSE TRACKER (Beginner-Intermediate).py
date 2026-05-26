# expense_tracker.py
import csv
import os
from datetime import datetime
from collections import defaultdict

class ExpenseTracker:
    def __init__(self):
        self.filename = "expenses.csv"
        self.categories = ["Food", "Transport", "Entertainment", "Bills", "Shopping", "Other"]
        self.initialize_file()
    
    def initialize_file(self):
        """Create CSV file with headers if not exists"""
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Date", "Category", "Amount", "Description"])
    
    def add_expense(self):
        """Add a new expense"""
        print("\n📝 Add New Expense")
        
        # Show categories
        print("\nCategories:")
        for i, cat in enumerate(self.categories, 1):
            print(f"  {i}. {cat}")
        
        try:
            cat_choice = int(input("Choose category (1-6): ")) - 1
            category = self.categories[cat_choice] if 0 <= cat_choice < len(self.categories) else "Other"
            
            amount = float(input("Amount: $"))
            if amount <= 0:
                print("❌ Amount must be positive!")
                return
            
            description = input("Description: ")
            date = datetime.now().strftime("%Y-%m-%d")
            
            # Save to CSV
            with open(self.filename, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([date, category, amount, description])
            
            print(f"✅ Expense added: ${amount} for {category}")
            
        except ValueError:
            print("❌ Invalid input!")
    
    def view_summary(self):
        """View expense summary"""
        if not os.path.exists(self.filename):
            print("No expenses recorded yet!")
            return
        
        expenses = []
        with open(self.filename, 'r') as f:
            reader = csv.DictReader(f)
            expenses = list(reader)
        
        if not expenses:
            print("No expenses found!")
            return
        
        # Calculate totals
        total = 0
        category_totals = defaultdict(float)
        
        for expense in expenses:
            amount = float(expense["Amount"])
            total += amount
            category_totals[expense["Category"]] += amount
        
        print("\n" + "="*50)
        print("📊 EXPENSE SUMMARY")
        print("="*50)
        print(f"💰 Total Expenses: ${total:.2f}")
        print(f"📋 Number of Transactions: {len(expenses)}")
        print("\n📂 By Category:")
        print("-"*30)
        
        for category, amount in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
            percentage = (amount / total) * 100 if total > 0 else 0
            print(f"  {category:<15}: ${amount:>8.2f} ({percentage:>5.1f}%)")
        
        # Show recent expenses
        print("\n📅 Recent Expenses (Last 5):")
        print("-"*50)
        print(f"{'Date':<12} {'Category':<12} {'Amount':<8} {'Description'}")
        print("-"*50)
        for expense in expenses[-5:]:
            print(f"{expense['Date']:<12} {expense['Category']:<12} ${float(expense['Amount']):<7.2f} {expense['Description']}")
    
    def monthly_report(self):
        """Generate monthly report"""
        month = input("Enter month (MM) or press Enter for current: ")
        if not month:
            month = datetime.now().strftime("%m")
        
        year = datetime.now().strftime("%Y")
        
        if not os.path.exists(self.filename):
            print("No expenses recorded yet!")
            return
        
        monthly_expenses = []
        with open(self.filename, 'r') as f:
            reader = csv.DictReader(f)
            for expense in reader:
                if expense['Date'].startswith(f"{year}-{month}"):
                    monthly_expenses.append(expense)
        
        if not monthly_expenses:
            print(f"No expenses for {year}-{month}")
            return
        
        total = sum(float(e['Amount']) for e in monthly_expenses)
        print(f"\n📅 Report for {year}-{month}")
        print(f"💰 Total: ${total:.2f}")
        print(f"📊 Transactions: {len(monthly_expenses)}")

def main():
    tracker = ExpenseTracker()
    while True:
        print("\n💰 EXPENSE TRACKER")
        print("1. Add Expense")
        print("2. View Summary")
        print("3. Monthly Report")
        print("4. Exit")
        
        choice = input("Choose (1-4): ")
        
        if choice == "1":
            tracker.add_expense()
        elif choice == "2":
            tracker.view_summary()
        elif choice == "3":
            tracker.monthly_report()
        elif choice == "4":
            print("Goodbye! 👋")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()