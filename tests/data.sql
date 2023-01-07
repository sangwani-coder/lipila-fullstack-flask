INSERT INTO school (job, school, email, mobile, reg_number, firstname, lastname, password)
VALUES
  ('administrator', 'academy', 'zyambo@icloud.com', '369854200','1245659', 'pita', 'zyambo', 'pbkdf2:sha256:260000$6gxuUEDjdUJnXzH5$83e1b2e1086c32d629d8f9de0b9a4ea3434fc3e8a48eefa086c696a12eff71bc'),
  ('director', 'switch academy', 'elsonpzyambo@gmail.com', '123456','123456', 'sangwani', 'zyambos', 'pbkdf2:sha256:260000$6gxuUEDjdUJnXzH5$83e1b2e1086c32d629d8f9de0b9a4ea3434fc3e8a48eefa086c696a12eff71bc');

INSERT INTO student(firstname, lastname, school, program, tuition)
VALUES 
  ('sepi', 'zed', 1, 'IT', 300),
  ('pita', 'zed', 1, 'IT', 300),
  ('mule', 'mule', 1, 'IT', 300),
  ('joe', 'kang', 1, 'IT', 300),
  ('willi', 'zyambo', 1, 'IT', 300),
  ('pita', 'zed', 1, 'IT', 300),
  ('mabu', 'chizya', 1, 'IT', 300),
  ('sepiso', 'muke', 1, 'IT', 300),
  ('nasi', 'lishebo', 1, 'IT', 300),
  ('nalishebo', 'zed', 1, 'IT', 300),
  ('george', 'kangwa', 1, 'IT', 300),
  ('papa', 'mumba', 1, 'IT', 300),
  ('jameson', 'mwale', 1, 'IT', 300),
  ('sangwa', 'zed', 2, 'MED', 300);

  INSERT INTO payment(student_id, firstname, lastname, amount, school, account_number)
VALUES 
  (1,'sepi','zed', 500, 1, '0971892260'),
  (2,'pita','zed', 500, 1, '0966698594'),
  (3, 'sangwa','zed', 500, 2, '0779069854'),
  (2,'pita','zed', 500, 1, '0966698594'),
  (2,'pita','zed', 500, 1, '0966698594'),
  (2,'pita','zed', 500, 1, '0966698594'),
  (1,'sepi','zed', 800, 1, '0966698594'),
  (2,'pita','zed', 400, 1, '0966698594'),
  (2,'pita','zed', 7700, 2, '0966698594'),
  (3,'sangwa','zed', 300, 2, '0966698594'),
  (1,'sepi','zed', 600, 1, '0966698594');
