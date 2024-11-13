#Expense tracker - Assessment 1
'''Program will allow a user to add expenses and track a budget.  All data is stored in a .csv file.
The .csv file will store the data even after the user exists the program, so they can come revisit their
Expense report.'''

#Imports libraries
import csv
import os
from datetime import datetime

#Function to prompt the user for expense details and store each entry as a dictionary in a list
def prompt_expense_details():
    expense_list = []
    while True:
        #Validates date format the user enters
        while True:
            date = input("Enter the date of the expense (YYYY-MM-DD): ").strip()
            try:
                datetime.strptime(date, "%Y-%m-%d")
                break
            except ValueError:
                print("Invalid date format. Please enter the date as YYYY-MM-DD.")

        category = input("Enter the category of the expense (e.g., Food, Travel): ").strip()
        
        #Ensure the expense amount entered is a valid positive integer
        while True:
            try:
                amount = int(input("Enter the amount spent (positive integer): ").strip())
                if amount > 0:
                    break
                else:
                    print("Please enter a positive number for the amount.")
            except ValueError:
                print("That is an invalid entry. Please enter a valid positive integer for the amount.")

        description = input("Enter a brief description of the expense: ").strip()
        
        #Stores the expense in a .csv file as a dictionary
        expense = {
            'date': date,
            'category': category,
            'amount': amount,
            'description': description
        }
        
        expense_list.append(expense)
        
        more_expenses = input("Would you like to add another expense? (Y/N): ").strip().upper()
        if more_expenses != 'Y':
            break
    
    return expense_list

#Function to view and validate expenses
def view_expenses(data):
    if not data:
        print("\nNo expenses recorded.")
        return

    print("\nStored Expenses:")
    for i, expense in enumerate(data, start=1):
        if all(key in expense and expense[key] for key in ['date', 'category', 'amount', 'description']):
            print(f"\nExpense {i}:")
            print(f"  Date: {expense['date']}")
            print(f"  Category: {expense['category']}")
            print(f"  Amount: ${float(expense['amount']):.2f}")
            print(f"  Description: {expense['description']}")
        else:
            print(f"\nExpense {i} is incomplete and will not be displayed (missing date, category, amount, or description).")

#Function to set a monthly budget
def set_monthly_budget():
    while True:
        try:
            budget = float(input("Enter your total monthly budget: ").strip())
            if budget <= 0:
                print("Please enter a positive number for the budget.")
            else:
                print(f"\nMonthly budget set to ${budget:.2f}")
                return budget
        except ValueError:
            print("Please enter a valid number for the budget.")

#Function to calculate the total expenses so far
def calculate_total_expenses(data):
    total = sum(float(expense['amount']) for expense in data if 'amount' in expense and expense['amount'])
    return total

#Function to track and compare expenses to the budget
def track_budget(data, budget):
    total_expenses = calculate_total_expenses(data)
    print(f"\nTotal expenses so far: ${total_expenses:.2f}")

    #Prints if budget is exceeded
    if total_expenses > budget:
        print("Oops! You have exceeded your budget!")
    #Prints if budget is within limits
    else:
        remaining = budget - total_expenses
        print(f"You have ${remaining:.2f} left for the month.")

#Function to save expenses to a CSV file
def save_expenses_to_csv(data, filename="data.csv"):
    if not data:
        print("\nNo data to save.")
        return

    #Keys/headers of csv file
    try:
        keys = ["date", "category", "amount", "description"]
        with open(filename, mode='w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            dict_writer.writeheader()
            for expense in data:
                expense['amount'] = f"{float(expense['amount']):.2f}"
                dict_writer.writerow(expense)
        print(f"\nExpenses successfully saved to {filename}")
    except Exception as e:
        print(f"\nAn error occurred while saving to {filename}: {e}")

#Function to load previous expenses from a CSV file
def load_expenses_from_csv(filename="data.csv"):
    data = []
    if not os.path.exists(filename):
        print(f"\nNo existing data file found. A new file will be created when you save expenses.")
        return data

    try:
        with open(filename, mode='r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row['amount'] = float(row['amount'])
                data.append(row)
        print(f"Loaded existing data from {filename}.")
    except Exception as e:
        print(f"\nAn error occurred while loading data from {filename}: {e}")

    return data

#Function to display the main menu and handle user choices
def display_menu(data, budget):
    while True:
        print("\nExpense Tracker Menu:")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Track Budget")
        print("4. Save Expenses")
        print("5. Exit")
        
        #Prompt to ask the user to choose what they'd like to do
        choice = input("Enter the number of your choice: ").strip()
        
        if choice == "1":
            new_expenses = prompt_expense_details()
            data.extend(new_expenses)
            print("\nNew expense(s) added successfully!")
        elif choice == "2":
            view_expenses(data)
        elif choice == "3":
            if budget is None:
                budget = set_monthly_budget()
            track_budget(data, budget)
        elif choice == "4":
            save_expenses_to_csv(data)
        elif choice == "5":
            save_expenses_to_csv(data)
            print("\nTerminating program. Goodbye!")
            break
        else:
            print("\nInvalid input. Please enter a number between 1 and 5.")

def main():
    #Loads existing expenses from file
    data = load_expenses_from_csv()
    budget = None

    #Displays the menu and handle user interactions
    display_menu(data, budget)

#Calls the main function
if __name__ == "__main__":
    main()