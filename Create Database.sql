-- -----------------------------------------------------
-- Schema loginexample
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS loginexample;
CREATE SCHEMA loginexample;
USE loginexample;

-- -----------------------------------------------------
-- Table loginexample.users
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS loginexample.users (
  user_id INT NOT NULL AUTO_INCREMENT,
  username VARCHAR(20) NOT NULL UNIQUE,
  password_hash CHAR(64) NOT NULL COMMENT 'SHA256 password hash stored in hexadecimal (64 characters)',
  email VARCHAR(320) NOT NULL COMMENT 'Maximum email address length according to RFC5321 section 4.5.3.1 is 320 characters (64 for local-part, 1 for at sign, 255 for domain)',
  role ENUM('user', 'staff', 'admin') NOT NULL,
  PRIMARY KEY (user_id));