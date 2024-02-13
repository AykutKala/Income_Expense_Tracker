# Import library
import sqlite3

# Import date for expense and income
from datetime import datetime


# This function is for create a table (expense,expense category,income and income category)
def create_tables():
    connection = sqlite3.connect("budget.db")
    cursor = connection.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS expense_categories (id INTEGER PRIMARY KEY,category_name TEXT,description TEXT,expense_budget FLOAT)")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY,category_id INTEGER,expense_amount FLOAT,expense_date TEXT,description TEXT)")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS income_categories (id INTEGER PRIMARY KEY,category_name TEXT,description TEXT)")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS incomes (id INTEGER PRIMARY KEY,category_id INTEGER,income_amount FLOAT,income_date TEXT,description TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS financial_goal (id INTEGER PRIMARY KEY,goal_amount FLOAT)")
    connection.commit()
    connection.close()


# This function is for expense category(category name and description)
def add_expense_category():
    exp_category_name = input("Enter expense category name: ")
    exp_category_desc = input("Enter expense category description: ")

    connection = sqlite3.connect("budget.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO expense_categories (category_name, description) VALUES (?, ?)",
                   (exp_category_name, exp_category_desc))
    connection.commit()
    connection.close()
    print("Expense category added successfully!")


# This function shows all expenses
def show_all_expenses():
    connection = sqlite3.connect("budget.db")
    cursor = connection.cursor()

    # Join two table for seeing expense category name instead of expense category id
    # cursor.execute("SELECT * FROM expenses ")
    cursor.execute(
        "SELECT exp.id, ec.category_name, exp.expense_amount, exp.expense_date, exp.description FROM expenses exp JOIN expense_categories ec where exp.category_id = ec.id ")
    expenses = cursor.fetchall()
    for expense in expenses:
        print(expense)
    connection.close()


# This function is for sum of all expenses
def get_expenses_sum():
    connection = sqlite3.connect("budget.db")
    cursor = connection.cursor()
    cursor.execute("SELECT sum(expense_amount) FROM expenses")
    exp_amount_sum = cursor.fetchone()
    connection.close()

    # Convert float sum of the expense amount
    try:
        exp_sum = float(exp_amount_sum[0])
    except:
        exp_sum = float(0)
    return exp_sum


# This function shows all expense categories
def show_all_expense_categories():
    connection = sqlite3.connect("budget.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM expense_categories ")
    expense_categories = cursor.fetchall()
    for expense_category in expense_categories:
        print(expense_category)
    connection.close()


# This function expense Id from user
def get_expense_id_from_user():
    # Call all expenses function for seeing all expenses and expense id
    show_all_expenses()
    entered_exp_id = 0
    while True:
        try:
            entered_exp_id = int(input("Enter expense id: "))
            connection = sqlite3.connect("budget.db")
            cursor = connection.cursor()
            cursor.execute("SELECT id FROM expenses WHERE id=?", (entered_exp_id,))
            exp_id = cursor.fetchone()
            connection.close()

            if exp_id is None:
                print("Expense not found.")
            else:
                break
        except:
            print("Invalid expense id!")

    return entered_exp_id


# This function is  for get expense category id from user
def get_expense_category_id_from_user():
    """ Call all expense categories function for
    seeing all expense categories and expense categories id"""
    show_all_expense_categories()
    entered_exp_category_id = 0
    while True:
        try:
            entered_exp_category_id = int(input("Enter expense category id: "))
            connection = sqlite3.connect("budget.db")
            cursor = connection.cursor()
            cursor.execute("SELECT id FROM expense_categories WHERE id=?", (entered_exp_category_id,))
            exp_category_id = cursor.fetchone()
            connection.close()

            if exp_category_id is None:
                print("Expense category not found.")
            else:
                break
        except:
            print("Invalid expense category id!")
    return entered_exp_category_id


def expense_category_exists():
    """ Check if there are any expense categories """
    connection = sqlite3.connect("budget.db")
    cursor = connection.cursor()
    cursor.execute("SELECT count(*) FROM expense_categories")
    exp_category_count = cursor.fetchone()
    connection.close()

    if exp_category_count is None or exp_category_count[0] == 0:
        exp_category_exists = False
        print("There are no expense categories! Please add expense category first!")
    else:
        exp_category_exists = True

    return exp_category_exists


def income_category_exists():
    """ Check if there are any income categories """
    connection = sqlite3.connect("budget.db")
    cursor = connection.cursor()
    cursor.execute("SELECT count(*) FROM income_categories")
    inc_category_count = cursor.fetchone()
    connection.close()

    if inc_category_count is None or inc_category_count[0] == 0:
        inc_category_exists = False
        print("There are no income categories! Please add income category first!")
    else:
        inc_category_exists = True

    return inc_category_exists


# This function is for update expenses by expense id
def update_expense():
    expense_id = get_expense_id_from_user()
    new_exp_amount = 0
    while True:
        try:
            new_exp_amount = float(input("Enter new expense amount: "))
            if new_exp_amount >= 0:
                break
            else:
                print("Invalid amount value!")
        except:
            print("Invalid amount value!")

    connection = sqlite3.connect("budget.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE expenses SET expense_amount=? WHERE id=?", (new_exp_amount, expense_id))
    connection.commit()
    connection.close()
    print("Expense updated successfully!")


# This function is for deleting expense by expense id
def delete_expense():
    expense_id = get_expense_id_from_user()

    connection = sqlite3.connect("budget.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    connection.commit()
    connection.close()
    print("Expense deleted successfully!")


# This function is deleting all expenses in the category of user selection by category id
def delete_expenses_by_category(category_id):
    connection = sqlite3.connect("budget.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM expenses WHERE category_id=?", (category_id,))
    connection.commit()
    connection.close()


# This function is for deleting expense category
def delete_expense_category():
    category_id = get_expense_category_id_from_user()
    delete_expenses_by_category(category_id)

    connection = sqlite3.connect("budget.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM expense_categories WHERE id=?", (category_id,))
    connection.commit()
    connection.close()
    print("Expense category is deleted successfully!")


# Income methods
# get sum of the all incomes
def get_incomes_sum():
    connection = sqlite3.connect("budget.db")
    cursor = connection.cursor()
    cursor.execute("SELECT sum(income_amount) FROM incomes")
    inc_amount_sum = cursor.fetchone()
    connection.close()
    # try-except errors and convert to float sum of the incomes
    try:
        inc_sum = float(inc_amount_sum[0])
    except:
        inc_sum = float(0)
    return inc_sum


# This function is for get the financial goal
def get_financial_goal():
    connection = sqlite3.connect("budget.db")
    cursor = connection.cursor()
    cursor.execute("SELECT goal_amount FROM financial_goal")
    goal_amount_val = cursor.fetchone()
    connection.close()
    # try-except errors and convert to float goal amount
    try:
        goal_amount = float(goal_amount_val[0])
    except:
        goal_amount = float(0)
    return goal_amount


# This is for calculating budget
def calculate_budget():
    total_incomes = get_incomes_sum()
    total_expenses = get_expenses_sum()
    user_budget = total_incomes - total_expenses
    print(f"Your budget is: {user_budget}")


# This function is for seeing progress
def view_progress():
    total_incomes = get_incomes_sum()
    total_expenses = get_expenses_sum()
    user_budget = total_incomes - total_expenses
    user_goal = get_financial_goal()

    print(f"Your budget is: {user_budget}")
    print(f"Your goal is: {user_goal}")
    print(f"Your progress: {user_goal - user_budget}")
    if user_budget > user_goal:
        print(f"Your are in your financial goal!")
    else:
        print(f"You did not reach to your financial goal!")


# This function is for income categories and income description
def add_income_category():
    inc_category_name = input("Enter income category name: ")
    inc_category_desc = input("Enter income category description: ")

    connection = sqlite3.connect("budget.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO income_categories (category_name, description) VALUES (?, ?)",
                   (inc_category_name, inc_category_desc))
    connection.commit()
    connection.close()
    print("Income category added successfully!")


# adding income by category of the income
def add_income():
    inc_category_id = get_income_category_id_from_user()
    inc_amount = 0
    while True:
        try:
            inc_amount = float(input("Enter income amount: "))
            if inc_amount >= 0:
                break
            else:
                print("Invalid amount value!")
        except:
            print("Invalid amount value!")

    # This is for correct date format
    inc_date_is_correct = False
    inc_date = datetime.today()
    while not inc_date_is_correct:
        try:
            inc_date_entry = input("Income date(dd/mm/yyyy): ")
            inc_date_fields = inc_date_entry.split("/")
            inc_date = datetime(int(inc_date_fields[2]), int(inc_date_fields[1]), int(inc_date_fields[0]))
            inc_date_is_correct = True
        except:
            print("Invalid due date! please enter a valid date!\n")

    inc_desc = input("Enter income description: ")

    connection = sqlite3.connect("budget.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO incomes (category_id, income_amount, income_date, description) VALUES (?, ?, ?, ?)",
                   (inc_category_id, inc_amount, f"{inc_date.strftime('%d %b %Y')}", inc_desc))
    connection.commit()
    connection.close()
    print("Income added successfully!")


# This function shows all incomes
def show_all_incomes():
    connection = sqlite3.connect("budget.db")
    cursor = connection.cursor()
    # Join two tables for seeing income category name instead of the income category id
    cursor.execute("SELECT inc.id, ic.category_name, inc.income_amount, inc.income_date, inc.description FROM incomes"
                   " inc JOIN income_categories ic where inc.category_id = ic.id ")

    incomes = cursor.fetchall()
    for income in incomes:
        print(income)
    connection.close()


# This function shows all income categories
def show_all_income_categories():
    connection = sqlite3.connect("budget.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM income_categories ")
    income_categories = cursor.fetchall()
    for income_category in income_categories:
        print(income_category)
    connection.close()


# This function works for getting income id from user
def get_income_id_from_user():
    show_all_incomes()
    entered_income_id = 0
    while True:
        try:
            entered_income_id = int(input("Enter income id: "))
            connection = sqlite3.connect("budget.db")
            cursor = connection.cursor()
            cursor.execute("SELECT id FROM incomes WHERE id=?", (entered_income_id,))
            income_id = cursor.fetchone()
            connection.close()

            if income_id is None:
                print("Income not found.")
            else:
                break
        except:
            print("Invalid income id!")

    return entered_income_id


# This function is for getting income category id from user
def get_income_category_id_from_user():
    # Call all income categories
    show_all_income_categories()
    entered_income_category_id = 0
    while True:
        try:
            entered_income_category_id = int(input("Enter income id: "))
            connection = sqlite3.connect("budget.db")
            cursor = connection.cursor()
            cursor.execute("SELECT id FROM income_categories WHERE id=?", (entered_income_category_id,))
            income_category_id = cursor.fetchone()
            connection.close()

            if income_category_id is None:
                print("Income category not found.")
            else:
                break
        except:
            print("Invalid income category id!")
    return entered_income_category_id


# This is for updating income by income id
def update_income():
    income_id = get_income_id_from_user()
    new_income_amount = 0
    while True:
        try:
            new_income_amount = float(input("Enter new income amount: "))
            if new_income_amount >= 0:
                break
            else:
                print("Invalid amount value!")
        except:
            print("Invalid amount value!")

    connection = sqlite3.connect("budget.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE expenses SET income_amount=? WHERE id=?", (new_income_amount, income_id))
    connection.commit()
    connection.close()
    print("Income updated successfully!")


# This function deletes income by income id
def delete_income():
    income_id = get_income_id_from_user()

    connection = sqlite3.connect("budget.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM incomes WHERE id=?", (income_id,))
    connection.commit()
    connection.close()
    print("Income deleted successfully!")


# This function is deleting all incomes in the category of user selection by category id
def delete_incomes_by_category(category_id):
    connection = sqlite3.connect("budget.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM incomes WHERE category_id=?", (category_id,))
    connection.commit()
    connection.close()


# This function deletes wanted income category
def delete_income_category():
    category_id = get_income_category_id_from_user()
    delete_incomes_by_category(category_id)

    connection = sqlite3.connect("budget.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM income_categories WHERE id=?", (category_id,))
    connection.commit()
    connection.close()
    print("Income category is deleted successfully!")


# This function is for getting user's financial goal
def set_financial_goal():
    goal_amount = 0  # Try - except for valid input expense budget
    while True:
        try:
            goal_amount = float(input("Enter goal amount: "))
            if goal_amount >= 0:
                break
            else:
                print("Invalid goal amount value!")
        except:
            print("Invalid goal amount value!")

    connection = sqlite3.connect("budget.db")
    cursor = connection.cursor()
    cursor.execute("INSERT OR REPLACE INTO financial_goal (id, goal_amount) VALUES (?, ?)", (1, goal_amount))
    connection.commit()
    connection.close()
    print("Financial goal set successfully!")


# Get budget from user for categories
def add_expense_category_budget():
    category_id = get_expense_category_id_from_user()
    exp_budget_amount = 0  # Try - except for valid input expense budget
    while True:
        try:
            exp_budget_amount = float(input("Enter expense budget amount: "))
            if exp_budget_amount >= 0:
                break
            else:
                print("Invalid budget amount value!")
        except:
            print("Invalid budget amount value!")

    connection = sqlite3.connect("budget.db")
    cursor = connection.cursor()
    cursor.execute("UPDATE expense_categories SET expense_budget=? WHERE id=?", (exp_budget_amount, category_id))
    connection.commit()
    connection.close()
    print("Expense budget updated successfully!")


# See all budget category
def show_expense_budget_by_category():
    category_id = get_expense_category_id_from_user()
    connection = sqlite3.connect("budget.db")
    cursor = connection.cursor()
    cursor.execute("SELECT id , category_name, expense_budget FROM expense_categories WHERE id=?", (category_id,))
    expense_categories = cursor.fetchall()
    for expense_category in expense_categories:
        print(expense_category)
    connection.close()


# This function is for seeing all expenses by categories
def show_all_expenses_by_category():
    category_id = get_expense_category_id_from_user()
    connection = sqlite3.connect("budget.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT exp.id, ec.category_name, exp.expense_amount, exp.expense_date, exp.description FROM expenses exp JOIN expense_categories ec ON exp.category_id = ec.id WHERE ec.id =?", (category_id,))

    expenses = cursor.fetchall()
    for expense in expenses:
        print(expense)
    connection.close()


# # This function is for seeing all incomes by categories
def show_all_incomes_by_category():
    category_id = get_income_category_id_from_user()
    connection = sqlite3.connect("budget.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT inc.id, ic.category_name, inc.income_amount, inc.income_date, inc.description FROM incomes inc JOIN income_categories ic ON inc.category_id = ic.id WHERE ic.id =?", (category_id,))

    expenses = cursor.fetchall()
    for expense in expenses:
        print(expense)
    connection.close()

# This function is for adding expense
def add_expense():
    # User will add expense by expense category
    exp_category_id = get_expense_category_id_from_user()
    exp_amount = 0  # Try - except for valid input expense amount
    while True:
        try:
            exp_amount = float(input("Enter expense amount: "))
            if exp_amount >= 0:
                break
            else:
                print("Invalid amount value!")
        except:
            print("Invalid amount value!")

    # This is for correct format for date
    exp_date_is_correct = False
    exp_date = datetime.today()
    while not exp_date_is_correct:
        try:
            exp_date_entry = input("Expense date(dd/mm/yyyy): ")
            exp_date_fields = exp_date_entry.split("/")
            exp_date = datetime(int(exp_date_fields[2]), int(exp_date_fields[1]), int(exp_date_fields[0]))
            exp_date_is_correct = True
        except:
            print("Invalid due date! please enter a valid date!\n")

    exp_desc = input("Enter expense description: ")

    connection = sqlite3.connect("budget.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO expenses (category_id, expense_amount, expense_date, description) VALUES (?, ?, ?, ?)",
                   (exp_category_id, exp_amount, f"{exp_date.strftime('%d %b %Y')}", exp_desc))
    connection.commit()
    connection.close()
    print("Expense added successfully!")


# Define user selection menu
create_tables()
while True:
    print("\nMenu:")
    print("1. Add expense category")
    print("2. Remove expense category")
    print("3. Add expense")
    print("4. Update expense")
    print("5. Remove expense")
    print("6. Show all expenses")
    print("7. Add income category")
    print("8. Remove income category")
    print("9. Add income")
    print("10. Update income")
    print("11. Remove income")
    print("12. Show all incomes")
    print("13. Show user budget")
    print("14. Set budget for a category")
    print("15. View budget for a category")
    print("16. Set financial goal")
    print("17. View progress")
    print("18. View expenses by category")
    print("19. View incomes by category")
    print("0. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_expense_category()
    elif choice == "2":
        if expense_category_exists():
            delete_expense_category()
    elif choice == "3":
        if expense_category_exists():
            add_expense()
    elif choice == "4":
        if expense_category_exists():
            update_expense()
    elif choice == "5":
        if expense_category_exists():
            delete_expense()
    elif choice == "6":
        show_all_expenses()
    elif choice == "7":
        add_income_category()
    elif choice == "8":
        if income_category_exists():
            delete_income_category()
    elif choice == "9":
        if income_category_exists():
            add_income()
    elif choice == "10":
        if income_category_exists():
            update_income()
    elif choice == "11":
        if income_category_exists():
            delete_income()
    elif choice == "12":
        show_all_incomes()
    elif choice == "13":
        calculate_budget()
    elif choice == "14":
        if expense_category_exists():
            add_expense_category_budget()
    elif choice == "15":
        if expense_category_exists():
            show_expense_budget_by_category()
    elif choice == "16":
        set_financial_goal()
    elif choice == "17":
        view_progress()
    elif choice == "18":
        if expense_category_exists():
            show_all_expenses_by_category()
    elif choice == "19":
        if income_category_exists():
            show_all_incomes_by_category()
    elif choice == "0":
        break
    else:
        print("Invalid choice. Please try again.")