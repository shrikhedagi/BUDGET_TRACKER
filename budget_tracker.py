import csv
import matplotlib.pyplot as plt
from datetime import datetime

# File to store the budget data
DATA_FILE = 'data.csv'

# Function to load data from CSV file
def load_data():
    transactions = []
    try:
        with open(DATA_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row['amount'] = float(row['amount'])
                row['date'] = datetime.strptime(row['date'], '%Y-%m-%d')
                transactions.append(row)
    except FileNotFoundError:
        pass
    return transactions

# Function to save data to CSV file
def save_data(transactions):
    with open(DATA_FILE, mode='w', newline='') as file:
        fieldnames = ['date', 'category', 'description', 'amount', 'type']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for transaction in transactions:
            writer.writerow({
                'date': transaction['date'].strftime('%Y-%m-%d'),
                'category': transaction['category'],
                'description': transaction['description'],
                'amount': transaction['amount'],
                'type': transaction['type']
            })

# Function to clear all data
def clear_data():
    open(DATA_FILE, 'w').close()  # This will clear the file
    print("All data has been cleared.")

# Function to add a transaction
def add_transaction(transactions, category, description, amount, transaction_type):
    transaction = {
        'date': datetime.now(),
        'category': category,
        'description': description,
        'amount': amount,
        'type': transaction_type
    }
    transactions.append(transaction)
    save_data(transactions)

# Function to summarize expenses and income
def summarize(transactions):
    summary = {'Income': 0, 'Expenses': 0}
    for transaction in transactions:
        if transaction['type'] == 'Income':
            summary['Income'] += transaction['amount']
        elif transaction['type'] == 'Expense':
            summary['Expenses'] += transaction['amount']
    return summary

# Function to visualize expenses by category
def visualize_expenses(transactions):
    categories = {}
    for transaction in transactions:
        if transaction['type'] == 'Expense':
            if transaction['category'] in categories:
                categories[transaction['category']] += transaction['amount']
            else:
                categories[transaction['category']] = transaction['amount']
    
    # Plotting the data
    if categories:
        plt.figure(figsize=(10, 6))
        plt.bar(categories.keys(), categories.values())
        plt.xlabel('Category')
        plt.ylabel('Amount Spent')
        plt.title('Expenses by Category')
        plt.show()
    else:
        print("No expenses to visualize.")

def main():
    transactions = load_data()

    while True:
        print("\nPersonal Budget Tracker")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Summary")
        print("4. Visualize Expenses")
        print("5. Clear All Data")
        print("6. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            category = input("Enter income category: ")
            description = input("Enter description: ")
            amount = float(input("Enter amount: "))
            add_transaction(transactions, category, description, amount, 'Income')
            print("Income added successfully.")

        elif choice == '2':
            category = input("Enter expense category: ")
            description = input("Enter description: ")
            amount = float(input("Enter amount: "))
            add_transaction(transactions, category, description, amount, 'Expense')
            print("Expense added successfully.")

        elif choice == '3':
            summary = summarize(transactions)
            print(f"Total Income: {summary['Income']}")
            print(f"Total Expenses: {summary['Expenses']}")
            print(f"Net Savings: {summary['Income'] - summary['Expenses']}")

        elif choice == '4':
            visualize_expenses(transactions)

        elif choice == '5':
            clear_data()
            transactions = []  # Reset the transactions list

        elif choice == '6':
            print("Exiting...")
            break

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
