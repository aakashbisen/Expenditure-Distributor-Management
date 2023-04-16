import logging
from flask import Flask, request
from models import db, User, Group, GroupUser, Expense, Approval

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://my_python_proj:password123@db4free.net/expense_service'
db.init_app(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/users', methods=['POST'])
def create_user():
    # Parse the request data
    data = request.get_json()
    name = data['name']
    email = data['email']

    # Create a new user
    user = User(name=name, email=email)
    db.session.add(user)
    db.session.commit()

    # Log the action
    logger.info(f'Created user with ID {user.id}')

    # Return the ID of the newly created user
    return {'id': user.id}

@app.route('/groups', methods=['POST'])
def create_group():
    # Parse the request data
    data = request.get_json()
    name = data['name']
    user_ids = data['user_ids']

    # Create a new group
    group = Group(name=name)
    db.session.add(group)
    db.session.commit()

    # Add users to the group
    for user_id in user_ids:
        group_user = GroupUser(group_id=group.id, user_id=user_id)
        db.session.add(group_user)

    db.session.commit()

    # Log the action
    logger.info(f'Created group with ID {group.id}')

    # Return the ID of the newly created group
    return {'id': group.id}


@app.route('/expenses', methods=['POST'])
def add_expense():
    # Parse the request data
    data = request.get_json()
    amount = data['amount']
    description = data['description']
    user_id = data['user_id']

    # Create a new expense
    expense = Expense(amount=amount, description=description, user_id=user_id)
    db.session.add(expense)
    db.session.commit()

    # Log the action
    logger.info(f'Added expense with ID {expense.id}')

    # Return the ID of the newly added expense
    return {'id': expense.id}


@app.route('/approvals', methods=['POST'])
def approve_expense():
    # Parse the request data
    data = request.get_json()
    expense_id = data['expense_id']
    user_id = data['user_id']

    # Create a new approval
    approval = Approval(expense_id=expense_id, user_id=user_id)
    db.session.add(approval)
    db.session.commit()

    # Log the action
    logger.info(f'Approved expense with ID {expense_id} by user with ID {user_id}')

    # Return an empty response
    return {}


@app.route('/groups/<int:group_id>/distribute', methods=['POST'])
def distribute_expenses(group_id):
    # Retrieve the group from the database
    group = db.session.query(Group).get(group_id)

    # Calculate the total expenses for the group
    total_expenses = 0
    for user in group.users:
        expenses = Expense.query.filter_by(user_id=user.id).all()
        total_expenses += sum(expense.amount for expense in expenses)

    # Calculate the per-person amount
    per_person_amount = total_expenses / len(group.users)

    # Distribute the expenses evenly among the group members
    for user in group.users:
        expenses = Expense.query.filter_by(user_id=user.id).all()
        total_amount = sum(expense.amount for expense in expenses)
        difference = per_person_amount - total_amount

        if difference > 0:
            # User owes money
            pass
        elif difference < 0:
            # User is owed money
            pass

    # Log the action
    logger.info(f'Distributed expenses for group with ID {group_id}')

    # Return an empty response
    return {}


@app.route('/users/<int:user_id>/statistics')
def view_statistics(user_id):
    # Retrieve the user's expenses from the database
    expenses = Expense.query.filter_by(user_id=user_id).all()

    # Calculate the total amount of the user's expenses
    total_amount = sum(expense.amount for expense in expenses)

    # Calculate the average amount of the user's expenses
    average_amount = total_amount / len(expenses) if expenses else 0

    # Calculate the number of expenses for the user
    num_expenses = len(expenses)

    # Log the action
    logger.info(f'Viewed statistics for user with ID {user_id}')

    # Return the statistics for the user
    return {
        'total_amount': total_amount,
        'average_amount': average_amount,
        'num_expenses': num_expenses
    }


if __name__ == '__main__':
    app.run()
