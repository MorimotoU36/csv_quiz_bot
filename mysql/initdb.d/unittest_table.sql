USE quiz_db;

CREATE TABLE IF NOT EXISTS unit_test
(
  quiz_num INT NOT NULL PRIMARY KEY,
  quiz_sentense VARCHAR(256) NOT NULL,
  answer VARCHAR(256) NOT NULL,
  clear_count INT DEFAULT 0,
  fail_count INT DEFAULT 0,
  category VARCHAR(256),
  img_file VARCHAR(128),
  checked BOOLEAN DEFAULT 0,
  deleted BOOLEAN DEFAULT 0
) DEFAULT CHARACTER
  SET=utf8;

DROP VIEW IF EXISTS unit_test_view;
CREATE VIEW unit_test_view AS 
SELECT 
  quiz_num,
  quiz_sentense,
  answer,
  clear_count,
  fail_count,
  category,
  img_file,
  checked,
  deleted,
  100 * clear_count / (clear_count + fail_count) AS accuracy_rate
FROM unit_test;

DROP VIEW IF EXISTS unit_test_category_view;
CREATE VIEW unit_test_category_view AS 
SELECT 
  c.category as c_category,
  COUNT(*) as count,
  SUM(clear_count) as sum_of_clear_count,
  SUM(fail_count) as sum_of_fail_count,
  100 * SUM(clear_count) / (SUM(clear_count) + SUM(fail_count) ) AS accuracy_rate
FROM category as c 
CROSS JOIN unit_test as a 
WHERE c.file_name = 'unit_test' 
AND a.category LIKE concat('%',c.category,'%')
AND a.deleted != 1
GROUP BY c_category
ORDER BY c_category;
