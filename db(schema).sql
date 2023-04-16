USE expense_service;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(64) NOT NULL,
    email VARCHAR(64) NOT NULL
);

CREATE TABLE `groups` (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(64) NOT NULL
);

CREATE TABLE group_users (
    group_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (group_id) REFERENCES `groups`(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    PRIMARY KEY (group_id, user_id)
);

CREATE TABLE expenses (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    amount FLOAT NOT NULL,
    description VARCHAR(256) NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE approvals (
    expense_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (expense_id) REFERENCES expenses(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    PRIMARY KEY (expense_id, user_id)
);