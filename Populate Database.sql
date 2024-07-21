USE loginexample;

-- -----------------------------------------------------
-- Create Example Users
-- -----------------------------------------------------
-- User passwords are all just the username with "pass" appended:
--
-- User     Password
-- ------   --------
-- user1    user1pass
-- user2    user2pass
-- staff1   staff1pass
-- staff2   staff2pass
-- admin1   admin1pass
--
-- Hashes were generated using the included password_hash_generator.py script,
-- with the salt 'ExampleSaltValue'.
-- -----------------------------------------------------

INSERT INTO `loginexample`.`users` (`username`, `password_hash`, `email`, `role`) VALUES
    ('user1', '490cbfbe67bd8c617be3c6df6c829b6ac646ba3ae64f68f0a3cc284908855554', 'user1@example.com', 'user'),
    ('user2', '2ffa2992addbd26a22490cc0a9b4bf7fa5ba2f218fccd3a57aaf299b7aa93dd9', 'user2@example.com', 'user'),
    ('staff1', '6fcd6883408bf1760fd9f9953fe6b219d74488288de6b63a437bb2bdabb204f2', 'staff1@example.com', 'staff'),
    ('staff2', '37bb41f28154ad01ce2eac36cdd126385d173c9c7057587cee0fa78691f85aff', 'staff2@example.com', 'staff'),
    ('admin1', 'f96ccfe70a319f69019876d2be895235e7ee5d2b5f21dd51c6aa189b275acddf', 'admin1@example.com', 'admin');
