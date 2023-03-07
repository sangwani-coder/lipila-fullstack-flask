DROP TABLE IF EXISTS payment;
DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS school;
DROP TABLE IF EXISTS users;

-- Create user table to store a students information
CREATE TABLE IF NOT EXISTS users(
  id SERIAL PRIMARY KEY NOT NULL,
  email VARCHAR(255) UNIQUE,
  mobile VARCHAR(255),
  firstname VARCHAR(255),
  lastname VARCHAR(255),
  password VARCHAR(255) 
);

-- Create school table to store admin user details and 
-- Details of the school
CREATE TABLE IF NOT EXISTS school (
  id SERIAL PRIMARY KEY,
  job VARCHAR(255),
  created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  school VARCHAR(255) UNIQUE,
  email VARCHAR(255) UNIQUE,
  mobile VARCHAR(255),
  reg_number VARCHAR(255) UNIQUE,
  firstname VARCHAR(255),
  lastname VARCHAR(255),
  password VARCHAR(255) 
);

-- Create student table to store a
-- students information
CREATE TABLE IF NOT EXISTS student (
  id SERIAL PRIMARY KEY NOT NULL,
  payment_code VARCHAR(55),
  firstname VARCHAR(255),
  lastname VARCHAR(255),
  created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  school INTEGER,
  program VARCHAR(255),
  tuition INTEGER,
  constraint FK_student_school FOREIGN KEY (school) REFERENCES school (id) on delete cascade on update cascade
);

CREATE TABLE payment (
  id SERIAL PRIMARY KEY NOT NULL,
  student_id INTEGER,
  firstname VARCHAR(150),
  lastname VARCHAR(150),
  created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  amount INTEGER,
  term VARCHAR(15),
  years VARCHAR(6),
  account_number VARCHAR(255),
  school INTEGER,
  FOREIGN KEY (student_id) REFERENCES student (id) on delete cascade on update cascade,
  FOREIGN KEY (school) REFERENCES school (id) on delete cascade on update cascade
);
