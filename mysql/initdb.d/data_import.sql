
SET GLOBAL local_infile=on;
grant all on quiz_db.* to 'root'@'localhost';

LOAD DATA LOCAL INFILE "/docker-entrypoint-initdb.d/aws_quiz_data.csv"
INTO TABLE aws_quiz 
FIELDS TERMINATED BY ',';

