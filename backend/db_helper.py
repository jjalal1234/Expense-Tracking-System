import mysql.connector
from contextlib import contextmanager
from logging_setup import setup_logger

# CRUD - C: Create, R: Retrieve, U: Update, D: Delete

logger = setup_logger("backend.db_helper")

@contextmanager
def get_db_cursor(commit=False):

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="expense_manager"
    )

    cursor = connection.cursor(dictionary=True)
    yield cursor

    if commit:
        connection.commit()

    cursor.close()
    connection.close()

def fetch_expenses_for_date(expenses_date):
    logger.info(f"fetch_expenses_for_date called with {expenses_date}")
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses where expense_date = %s", (expenses_date,))
        expenses = cursor.fetchall()
        return expenses

def insert_expense(expense_date, amount, category, notes):
    logger.info(f"insert_expense called with {expense_date}, {amount}, {category}, {notes}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO expenses (expense_date, amount, category, notes) values (%s, %s, %s, %s)",
            (expense_date, amount, category, notes)
        )

def delete_expenses_for_date(expense_date):
    logger.info(f"delete_expenses_for_date called with {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date,))

def fetch_expense_summary(start_date, end_date):
    logger.info(f"fetch_expense_summary called with start date: {start_date}, end_date {end_date}")
    with get_db_cursor() as cursor:
        cursor.execute(
            '''select category, sum(amount) as total
            from expense_manager.expenses where expense_date
            between %s and %s
            group by category;''',
            (start_date, end_date)
        )
        print("================")
        data = cursor.fetchall()
        return data

if __name__ == '__main__':
    # fetch_all_records()
    expense = fetch_expenses_for_date("2024-08-01")
    print(expense)
    #insert_expense("2024-08-28", "80", "Food", "Brisket")
    #print("==============")
    #delete_expenses_for_date("2024-08-28")
    summery =  fetch_expense_summary("2024-08-01", "2024-08-05")
    for expense in summery:
       print(expense)