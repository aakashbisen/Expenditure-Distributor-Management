import unittest
from flask_testing import TestCase
from app import app, db, User, Group, GroupUser, Expense, Approval


class AppTestCase(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://my_python_proj:password123@db4free.net/expense_service'
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        # db.drop_all()

    def test_create_user(self):
        # Create a test user
        response = self.client.post('/users', json={
            'name': 'Test User',
            'email': 'test@example.com'
        })
        data = response.get_json()

        # Verify that the user was created successfully
        self.assertEqual(response.status_code, 200)
        self.assertIn('id', data)

        user_id = data['id']
        user = db.session.query(User).get(user_id)
        self.assertIsNotNone(user)
        self.assertEqual(user.name, 'Test User')
        self.assertEqual(user.email, 'test@example.com')

    def test_create_group(self):
        # Create a test user
        user = User(name='Test User', email='test@example.com')
        db.session.add(user)
        db.session.commit()

        # Create a test group
        response = self.client.post('/groups', json={
            'name': 'Test Group',
            'user_ids': [user.id]
        })
        data = response.get_json()

        # Verify that the group was created successfully
        self.assertEqual(response.status_code, 200)
        self.assertIn('id', data)

        group_id = data['id']
        group = db.session.query(Group).get(group_id)
        self.assertIsNotNone(group)
        self.assertEqual(group.name, 'Test Group')
        self.assertEqual(len(group.users), 1)
        self.assertEqual(group.users[0].id, user.id)

    def test_add_expense(self):
        # Create a test user
        user = User(name='Test User', email='test@example.com')
        db.session.add(user)
        db.session.commit()

        # Add a test expense
        response = self.client.post('/expenses', json={
            'amount': 10.0,
            'description': 'Test Expense',
            'user_id': user.id
        })
        data = response.get_json()

        # Verify that the expense was added successfully
        self.assertEqual(response.status_code, 200)
        self.assertIn('id', data)

        expense_id = data['id']
        expense = db.session.query(Expense).get(expense_id)
        self.assertIsNotNone(expense)
        self.assertEqual(expense.amount, 10.0)
        self.assertEqual(expense.description, 'Test Expense')
        self.assertEqual(expense.user_id, user.id)

    def test_approve_expense(self):
        # Create a test user
        user = User(name='Test User', email='test@example.com')
        db.session.add(user)
        db.session.commit()

        # Add a test expense
        expense = Expense(amount=10.0, description='Test Expense', user_id=user.id)
        db.session.add(expense)
        db.session.commit()

        # Approve the test expense
        response = self.client.post('/approvals', json={
            'expense_id': expense.id,
            'user_id': user.id
        })

        # Verify that the expense was approved successfully
        self.assertEqual(response.status_code, 200)

        approval = Approval.query.filter_by(expense_id=expense.id, user_id=user.id).first()
        self.assertIsNotNone(approval)

    def test_view_statistics(self):
        # Create a test user
        user = User(name='Test User', email='test@example.com')
        db.session.add(user)
        db.session.commit()

        # Add test expenses for the user
        expense1 = Expense(amount=10.0, description='Test Expense 1', user_id=user.id)
        expense2 = Expense(amount=20.0, description='Test Expense 2', user_id=user.id)
        db.session.add(expense1)
        db.session.add(expense2)
        db.session.commit()

        # View the statistics for the user
        response = self.client.get(f'/users/{user.id}/statistics')

        # Verify that the statistics were retrieved successfully
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertEqual(data['total_amount'], 30.0)
        self.assertEqual(data['average_amount'], 15.0)
        self.assertEqual(data['num_expenses'], 2)


if __name__ == '__main__':
    unittest.main()
