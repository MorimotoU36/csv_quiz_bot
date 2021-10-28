CREATE DATABASE IF NOT EXISTS quiz_db;
USE quiz_db;
DROP DATABASE IF EXISTS testdb;

CREATE TABLE IF NOT EXISTS aws_quiz
(
  quiz_num INT NOT NULL PRIMARY KEY,
  quiz_sentense VARCHAR(256) NOT NULL,
  answer VARCHAR(256) NOT NULL,
  clear_count INT DEFAULT 0,
  fail_count INT DEFAULT 0,
  category VARCHAR(256),
  img_file VARCHAR(128)
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
  img_file VARCHAR(128)
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
  img_file VARCHAR(128)
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
  img_file VARCHAR(128)
) DEFAULT CHARACTER
  SET=utf8;