USE quiz_db;
SELECT * FROM aws_quiz INTO OUTFILE '/docker-entrypoint-initdb.d/export_data/aws_quiz.csv';
SELECT * FROM applied INTO OUTFILE '/docker-entrypoint-initdb.d/export_data/applied.csv';
SELECT * FROM lpic INTO OUTFILE '/docker-entrypoint-initdb.d/export_data/lpic.csv';
SELECT * FROM category INTO OUTFILE '/docker-entrypoint-initdb.d/export_data/category.csv';

