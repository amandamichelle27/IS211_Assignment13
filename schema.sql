DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS quizzes;
DROP TABLE IF EXISTS quiz_scores;
DROP TABLE IF EXISTS user;

CREATE TABLE students (
    id          INTEGER  PRIMARY KEY AUTOINCREMENT,
    first_name  TEXT,
    last_name   TEXT
);

CREATE TABLE quizzes (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    subject        TEXT,
    num_questions  INTEGER,
    date           TEXT
);

CREATE TABLE quiz_scores (
    student_id   INTEGER,
    quiz_id      INTEGER,
    score        INTEGER,
    PRIMARY KEY (student_id, quiz_id),
    FOREIGN KEY(student_id) REFERENCES students(id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(quiz_id) REFERENCES quiz(id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE user (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
);

INSERT INTO students (id, first_name, last_name)
VALUES (1, "John", "Smith");

INSERT INTO quizzes (id, subject, num_questions, date)
VALUES (1, "Python Basics", 5, "2015-02-05");

INSERT INTO quiz_scores (student_id, quiz_id, score)
VALUES (1, 1, 85);

INSERT INTO user (username, password)
VALUES ("admin", "password");
