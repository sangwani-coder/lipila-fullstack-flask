INSERT INTO school (job, school, email, mobile, reg_number, firstname, lastname, password)
VALUES
  ('administrator', 'academy', 'pz@email.com', '369854200','1245659', 'pita', 'zyambo', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f'),
  ('a', 'a', 'a', 'a','a', 'a', 'a', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79');

INSERT INTO student(firstname, lastname, school, program, tuition)
VALUES 
  ('sepi', 'zed', 1, 'IT', 300),
  ('pita', 'zed', 1, 'IT', 300),
  ('sangwa', 'zed', 2, 'MED', 300);

  INSERT INTO payment(student_id, amount, account_number)
VALUES 
  (1, 300, '06969854'),
  (2, 500, '06969854'),
  (3, 300, '06969854');
