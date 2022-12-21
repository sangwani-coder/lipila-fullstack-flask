DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS payment;
DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS school;

-- Create user table to store a students information
CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE NOT NULL,
  mobile TEXT NOT NULL,
  firsname TEXT NOT NULL,
  lastname TEXT NOT NULL,
  password TEXT NOT NULL
);

-- Create school table to store admin user details and 
-- Details of the school
CREATE TABLE school (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  job TEXT NOT NULL,
  school TEXT UNIQUE NOT NULL,
  email TEXT UNIQUE NOT NULL,
  mobile TEXT NOT NULL,
  reg_number TEXT UNIQUE NOT NULL,
  firstname TEXT NOT NULL,
  lastname TEXT NOT NULL,
  password TEXT NOT NULL
);

-- Create student table to store a
-- students information
CREATE TABLE student (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  firstname TEXT NOT NULL,
  lastname TEXT NOT NULL,
  school TEXT NOT NULL,
  program TEXT NOT NULL,
  tuition INTEGER NOT NULL,
  FOREIGN KEY (school) REFERENCES school (id)
);

CREATE TABLE payment (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  student_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  amount INTEGER NOT NULL,
  account_number TEXT NOT NULL,
  FOREIGN KEY (student_id) REFERENCES student (id)
);


