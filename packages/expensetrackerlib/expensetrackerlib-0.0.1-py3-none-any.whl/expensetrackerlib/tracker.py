def calculate_total_expenses(expenses):
    total_amount = sum(expense.amount for expense in expenses)
    return total_amount