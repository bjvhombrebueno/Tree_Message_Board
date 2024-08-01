-- -----------------------------------------------------
-- Schema Tree_Message_Board
-- -----------------------------------------------------
-- DROP SCHEMA IF EXISTS `tmb`;
-- CREATE SCHEMA `tmb` DEFAULT CHARACTER SET utf8 ;
-- USE `tmb`;

-- -----------------------------------------------------
-- Table tmb.users
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `users` (
  `user_id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(20) NOT NULL UNIQUE,
  `password_hash` CHAR(64) NOT NULL COMMENT 'SHA256 password hash stored in hexadecimal (64 characters)',
  `email` VARCHAR(320) NOT NULL COMMENT 'Maximum email address length according to RFC5321 section 4.5.3.1 is 320 characters (64 for local-part, 1 for at sign, 255 for domain)',
  `first_name` VARCHAR(50) NOT NULL,
  `last_name` VARCHAR(50) NOT NULL,
  `birth_date` DATE NOT NULL,
  `location` VARCHAR(50) NOT NULL,
  `profile_image` VARCHAR(255),
  `role` ENUM('member', 'moderator', 'admin') NOT NULL,
  `status` ENUM('active', 'inactive') NOT NULL,
  PRIMARY KEY (`user_id`));
  
  
-- -----------------------------------------------------
-- Table tmb.messages
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `messages` (
  `message_id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `title` VARCHAR(255) NOT NULL,
  `content` TEXT NOT NULL,
  `created_at` TIMESTAMP NOT NULL,
  PRIMARY KEY (`message_id`),
  -- CONSTRAINT `fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `tmb`.`users` (`user_id`));
  FOREIGN KEY (`user_id`) REFERENCES `tmb`.`users` (`user_id`));

-- -----------------------------------------------------
-- Table tmb.replies
-- -----------------------------------------------------
 CREATE TABLE IF NOT EXISTS `replies` (
   `reply_id` INT NOT NULL AUTO_INCREMENT,
   `message_id` INT NOT NULL,
   `user_id` INT NOT NULL,
   `content` TEXT NOT NULL,
   `created_at` TIMESTAMP NOT NULL,
   PRIMARY KEY (`reply_id`),
  --  CONSTRAINT `fk_user_id2` FOREIGN KEY (`user_id`) REFERENCES `tmb`.`users` (`user_id`),
  --  CONSTRAINT `fk_message_id` FOREIGN KEY (`message_id`) REFERENCES `tmb`.`messages` (`message_id`));
   FOREIGN KEY (`user_id`) REFERENCES `tmb`.`users` (`user_id`),
   FOREIGN KEY (`message_id`) REFERENCES `tmb`.`messages` (`message_id`));
   
  