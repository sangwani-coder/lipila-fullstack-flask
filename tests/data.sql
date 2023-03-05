INSERT INTO school (job, school, email, mobile, reg_number, firstname, lastname, password)
VALUES
  ('administrator', 'academy', 'admin@email.com', '369854200','1245659', 'pita', 'zyambo', 'pbkdf2:sha256:260000$6gxuUEDjdUJnXzH5$83e1b2e1086c32d629d8f9de0b9a4ea3434fc3e8a48eefa086c696a12eff71bc'),
  ('director', 'switch academy', 'lipila@email.com', '123456','123456', 'sangwani', 'zyambos', 'pbkdf2:sha256:260000$6gxuUEDjdUJnXzH5$83e1b2e1086c32d629d8f9de0b9a4ea3434fc3e8a48eefa086c696a12eff71bc');

INSERT INTO student(payment_code, firstname, lastname, created, school, program, tuition)
VALUES 
  ('SZ23001','sepi', 'zed','2020-05-20 13:02:52.281964', 1, 'IT', 300),
  ('PZ23002','pita', 'zed','2020-05-20 13:02:52.281964', 1, 'IT', 300),
  ('MM23003','mule', 'mule','2020-05-20 13:02:52.281964', 1, 'IT', 300),
  ('JK23004','joe', 'kang','2020-05-20 13:02:52.281964', 1, 'IT', 300),
  ('WZ23005','willi', 'zyambo','2020-05-20 13:02:52.281964', 1, 'IT', 300),
  ('PZ23006','pita', 'zed','2021-01-10 10:52:52.281964', 1, 'IT', 300),
  ('MC23007','mabu', 'chizya','2021-01-10 10:52:52.281964', 1, 'IT', 300),
  ('SM23008','sepiso', 'muke','2021-01-10 10:52:52.281964', 1, 'IT', 300),
  ('NL23009','nasi', 'lishebo','2021-01-10 10:52:52.281964', 1, 'IT', 300),
  ('NZ23010','nalishebo', 'zed','2021-01-10 10:52:52.281964', 1, 'IT', 300),
  ('GK23011','george', 'kangwa','2023-01-10 10:52:52.281964', 1, 'IT', 300),
  ('PM23012','papa', 'mumba','2023-01-10 10:52:52.281964', 1, 'IT', 300),
  ('JM23013','jameson', 'mwale','2022-08-10 16:32:22.281964', 1, 'IT', 300),
  ('SZ23014','sangwa', 'zed','2029-01-10 10:52:52.281964', 2, 'MED', 300),
  ('JZ23015','Josh', 'zyambo','2021-05-20 13:02:52.281964', 2, 'Engr', 300);

  INSERT INTO payment(student_id, firstname, lastname, created, amount, school, account_number)
VALUES 
  (1,'sepi','zed','2020-05-20 13:02:52.281964', 500, 1, '0971892260'),
  (3, 'sangwa','zed','2023-01-20 10:55:52.281964', 500, 2, '0779069854'),
  (2,'pita','zed','2022-05-20 13:02:52.281964', 500, 1, '0966698594'),
  (2,'pita','zed','2021-05-20 13:02:52.281964', 500, 1, '0966698594'),
  (2,'pita','zed','2019-05-20 13:02:52.281964', 500, 1, '0966698594'),
  (1,'sepi','zed','2022-03-15 13:02:52.281964', 800, 1, '0966698594'),
  (2,'pita','zed','2021-05-20 13:02:52.281964', 400, 1, '0966698594'),
  (2,'pita','zed','2023-03-02 13:02:52.281964', 7700, 2, '0966698594'),
  (2,'pita','zed','2023-02-02 13:02:52.281964', 700, 2, '0966698594'),
  (3,'sangwa','zed','2022-05-20 13:02:52.281964', 300, 2, '0966698594'),
  (1,'sepi','zed','2022-10-20 13:02:52.281964', 600, 1, '0966698594');
