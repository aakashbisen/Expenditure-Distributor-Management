# Expense Service REST API Documentation

This is the documentation for the Expense Service REST API.

# Getting started:
* Install the required packages by running `pip install -r requirements.txt`.

* Set the Flask app environment variable by running `export FLASK_APP=app.py` (on Linux/Mac) or `set FLASK_APP=app.py` (on Windows).

* Start the Flask app by running the `app.py` file.

## API Endpoints

# Create User

`POST /users`

**Body:**
- `name` (string): The name of the user.
- `email` (string): The email of the user.

**Response:**
- `200`: The user was successfully created. Returns the ID of the newly created user.
- `400`: The request was invalid.

**Example:**

POST /users Content-Type: application/json

{ “name”: “John Doe”, “email”: “john.doe@example.com” }

200 OK Content-Type: application/json

{ “id”: 1 }

## Create Group

`POST /groups`

**Body:**
- `name` (string): The name of the group.
- `user_ids` (array of integers): The IDs of the users to add to the group.

**Response:**
- `200`: The group was successfully created. Returns the ID of the newly created group.
- `400`: The request was invalid.

**Example:**

POST /groups Content-Type: application/json

{ “name”: “My Group”, “user_ids”: [1, 2, 3] }

200 OK Content-Type: application/json

{ “id”: 1 }

## Add Expense

`POST /expenses`

**Body:**
- `amount` (float): The amount of the expense.
- `description` (string): The description of the expense.
- `user_id` (integer): The ID of the user who added the expense.

**Response:**
- `200`: The expense was successfully added. Returns the ID of the newly added expense.
- `400`: The request was invalid.

**Example:**

POST /expenses Content-Type: application/json

{ “amount”: 10.5, “description”: “Lunch”, “user_id”: 1 }

200 OK Content-Type: application/json

{ “id”: 1 }

## Approve Expense

`POST /approvals`

**Body:**
- `expense_id` (integer): The ID of the expense to approve.
- `user_id` (integer): The ID of the user who approved the expense.

**Response:**
- `200`: The expense was successfully approved.
- `400`: The request was invalid.

**Example:**

POST /approvals Content-Type: application/json

{ “expense_id”: 1, “user_id”: 2 }

200 OK Content-Type: application/json

## Distribute Expenses

`POST /groups/{group_id}/distribute`

**Path Parameters:**
- `group_id` (integer): The ID of the group to distribute expenses for.

**Response:**
- `200`: The expenses were successfully distributed.
- `400`: The request was invalid.

**Example:**

POST /groups/1/distribute Content-Type: application/json

200 OK Content-Type: application/json

## View Statistics

`GET /users/{user_id}/statistics`

**Path Parameters:**
- `user_id` (integer): The ID of the user to view statistics for.

**Response:**
- `200`: The statistics were successfully retrieved. Returns the total amount, average amount, and number of expenses for the user.
- `400`: The request was invalid.

**Example:**

GET /users/1/statistics Content-Type: application/json

200 OK Content-Type: application/json

{ “total_amount”: 10.5, “average_amount”: 5.25, “num_expenses”: 2 }