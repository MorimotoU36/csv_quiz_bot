CREATE DATABASE IF NOT EXISTS quiz_db;
USE quiz_db;

CREATE TABLE IF NOT EXISTS aws_quiz
(
  quiz_num INT NOT NULL PRIMARY KEY,
  quiz_sentense VARCHAR(256) NOT NULL,
  answer VARCHAR(256) NOT NULL,
  clear_count INT DEFAULT 0,
  fail_count INT DEFAULT 0,
  category VARCHAR(256),
  img_file VARCHAR(128),
  checked BOOLEAN DEFAULT 0
) DEFAULT CHARACTER
  SET=utf8;

CREATE TABLE IF NOT EXISTS applied
(
  quiz_num INT NOT NULL PRIMARY KEY,
  quiz_sentense VARCHAR(256) NOT NULL,
  answer VARCHAR(256) NOT NULL,
  clear_count INT DEFAULT 0,
  fail_count INT DEFAULT 0,
  category VARCHAR(256),
  img_file VARCHAR(128),
  checked BOOLEAN DEFAULT 0
) DEFAULT CHARACTER
  SET=utf8;

CREATE TABLE IF NOT EXISTS lpic
(
  quiz_num INT NOT NULL PRIMARY KEY,
  quiz_sentense VARCHAR(256) NOT NULL,
  answer VARCHAR(256) NOT NULL,
  clear_count INT DEFAULT 0,
  fail_count INT DEFAULT 0,
  category VARCHAR(256),
  img_file VARCHAR(128),
  checked BOOLEAN DEFAULT 0
) DEFAULT CHARACTER
  SET=utf8;

CREATE TABLE IF NOT EXISTS english_speaking
(
  quiz_num INT NOT NULL PRIMARY KEY,
  quiz_sentense VARCHAR(256) NOT NULL,
  answer VARCHAR(256) NOT NULL,
  clear_count INT DEFAULT 0,
  fail_count INT DEFAULT 0,
  category VARCHAR(256),
  img_file VARCHAR(128),
  checked BOOLEAN DEFAULT 0
) DEFAULT CHARACTER
  SET=utf8;

CREATE TABLE IF NOT EXISTS category
(
  file_name VARCHAR(256) NOT NULL,
  category VARCHAR(256) NOT NULL
) DEFAULT CHARACTER
  SET=utf8;

DROP VIEW IF EXISTS aws_quiz_view;
CREATE VIEW aws_quiz_view AS 
SELECT 
  quiz_num,
  quiz_sentense,
  answer,
  clear_count,
  fail_count,
  category,
  img_file,
  checked,
  100 * clear_count / (clear_count + fail_count) AS accuracy_rate
FROM aws_quiz;

DROP VIEW IF EXISTS applied_view;
CREATE VIEW applied_view AS 
SELECT 
  quiz_num,
  quiz_sentense,
  answer,
  clear_count,
  fail_count,
  category,
  img_file,
  checked,
  100 * clear_count / (clear_count + fail_count) AS accuracy_rate
FROM applied;

DROP VIEW IF EXISTS lpic_view;
CREATE VIEW lpic_view AS 
SELECT 
  quiz_num,
  quiz_sentense,
  answer,
  clear_count,
  fail_count,
  category,
  img_file,
  checked,
  100 * clear_count / (clear_count + fail_count) AS accuracy_rate
FROM lpic;

DROP VIEW IF EXISTS english_speaking_view;
CREATE VIEW english_speaking_view AS 
SELECT 
  quiz_num,
  quiz_sentense,
  answer,
  clear_count,
  fail_count,
  category,
  img_file,
  checked,
  100 * clear_count / (clear_count + fail_count) AS accuracy_rate
FROM english_speaking;

DROP VIEW IF EXISTS aws_quiz_category_view;
CREATE VIEW aws_quiz_category_view AS 
SELECT 
  c.category as c_category,
  COUNT(*) as count,
  SUM(clear_count) as sum_of_clear_count,
  SUM(fail_count) as sum_of_fail_count,
  SUM(clear_count) / (SUM(clear_count) + SUM(fail_count) ) AS accuracy_rate
FROM category as c 
CROSS JOIN aws_quiz as a 
WHERE c.file_name = 'aws_quiz' 
AND a.category LIKE concat('%',c.category,'%')
GROUP BY c_category
ORDER BY c_category;

DROP VIEW IF EXISTS applied_category_view;
CREATE VIEW applied_category_view AS 
SELECT 
  c.category as c_category,
  COUNT(*) as count,
  SUM(clear_count) as sum_of_clear_count,
  SUM(fail_count) as sum_of_fail_count,
  SUM(clear_count) / (SUM(clear_count) + SUM(fail_count) ) AS accuracy_rate
FROM category as c 
CROSS JOIN applied as a 
WHERE c.file_name = 'applied' 
AND a.category LIKE concat('%',c.category,'%')
GROUP BY c_category
ORDER BY c_category;

DROP VIEW IF EXISTS lpic_category_view;
CREATE VIEW lpic_category_view AS 
SELECT 
  c.category as c_category,
  COUNT(*) as count,
  SUM(clear_count) as sum_of_clear_count,
  SUM(fail_count) as sum_of_fail_count,
  SUM(clear_count) / (SUM(clear_count) + SUM(fail_count) ) AS accuracy_rate
FROM category as c 
CROSS JOIN lpic as a 
WHERE c.file_name = 'lpic' 
AND a.category LIKE concat('%',c.category,'%')
GROUP BY c_category
ORDER BY c_category;

DROP VIEW IF EXISTS english_speaking_category_view;
CREATE VIEW english_speaking_category_view AS 
SELECT 
  c.category as c_category,
  COUNT(*) as count,
  SUM(clear_count) as sum_of_clear_count,
  SUM(fail_count) as sum_of_fail_count,
  SUM(clear_count) / (SUM(clear_count) + SUM(fail_count) ) AS accuracy_rate
FROM category as c 
CROSS JOIN english_speaking as a 
WHERE c.file_name = 'english_speaking' 
AND a.category LIKE concat('%',c.category,'%')
GROUP BY c_category
ORDER BY c_category;

