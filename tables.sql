CREATE TABLE Users (
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    UserName TEXT NOT NULL,
    UserEmail TEXT NOT NULL UNIQUE,
    Password TEXT NOT NULL,
    Login_Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    todaystask TEXT NOT NULL,
    Tmember TEXT NOT NULL,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES Users (UserID)
);

INSERT INTO Users (UserName, UserEmail, Password)
VALUES 
('Alice', 'alice@example.com', 'password123'),
('Bob', 'bob@example.com', 'securepassword'),
('Charlie', 'charlie@example.com', 'charliepwd');



INSERT INTO todos (todaystask, Tmember, user_id)
VALUES 
('Complete project report', 'Alice', 1),
('Prepare presentation', 'Bob', 2),
('Review team performance', 'Charlie', 3),
('Organize team meeting', 'Alice', 1),
('Update website content', 'Bob', 2),
('Conduct code review', 'Charlie', 3);
