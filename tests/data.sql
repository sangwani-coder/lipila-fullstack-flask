INSERT INTO school (job, school, email, mobile, reg_number, firstname, lastname, password)
VALUES
  ('administrator', 'academy', 'admin@email.com', '369854200','1245659', 'pita', 'zyambo', 'pbkdf2:sha256:260000$6gxuUEDjdUJnXzH5$83e1b2e1086c32d629d8f9de0b9a4ea3434fc3e8a48eefa086c696a12eff71bc'),
  ('director', 'switch academy', 'lipila@email.com', '123456','123456', 'sangwani', 'zyambos', 'pbkdf2:sha256:260000$6gxuUEDjdUJnXzH5$83e1b2e1086c32d629d8f9de0b9a4ea3434fc3e8a48eefa086c696a12eff71bc');

INSERT INTO student(payment_code, firstname, lastname, school, program, tuition)
VALUES 
  ('SZ23001','sepi', 'zed', 1, 'IT', 300),
  ('PZ23002','pita', 'zed', 1, 'IT', 300),
  ('MM23003','mule', 'mule', 1, 'IT', 300),
  ('JK23004','joe', 'kang', 1, 'IT', 300),
  ('WZ23005','willi', 'zyambo', 1, 'IT', 300),
  ('PZ23006','pita', 'zed', 1, 'IT', 300),
  ('MC23007','mabu', 'chizya', 1, 'IT', 300),
  ('SM23008','sepiso', 'muke', 1, 'IT', 300),
  ('NL23009','nasi', 'lishebo', 1, 'IT', 300),
  ('NZ23010','nalishebo', 'zed', 1, 'IT', 300),
  ('GK23011','george', 'kangwa', 1, 'IT', 300),
  ('PM23012','papa', 'mumba', 1, 'IT', 300),
  ('JM23013','jameson', 'mwale', 1, 'IT', 300),
  ('SZ23014','sangwa', 'zed', 2, 'MED', 300);

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
