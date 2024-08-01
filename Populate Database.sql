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

INSERT INTO `tmb`.`users` (`username`, `password_hash`, `email`,`first_name`,`last_name`,`birth_date`,`location`,`profile_image`, `role`,`status`) VALUES
    ('q', 'c0f5955762c38545329a68b69ca288f78485ed0688d7cb0227085d9387f9ff63', 'user1@example.com','Aurora', 'Hayes','1990-05-03','UK','1','member','active'),
    ('w', '1388054c565184f9ec3fd9c513cab1b462e32cfb4089a22e0de1c6a7ccec49f6', 'user2@example.com','Caleb', 'Brooks','1992-12-01','Auckland','2','member','active'),
    ('a', '1762c21ca0f4a09591f67e584d8eb49eb35b8ecf3a6d1b19283efbe938055334', 'staff1@example.com','Serena', 'Yang','1985-07-23','Melbourne','3','moderator','active'),
    ('s', 'cdd02df61b7560b474935c00e0bfcba3905a99d2246f3060083d120df677132f', 'staff2@example.com','Declan', 'Ramirez','1989-04-05','Manila','4','moderator','active'),
    ('z', '8764663dced6e67a402365383654a427c5eb0cdf6f6428c0496c6d463b15cf08', 'admin1@example.com','Maya', 'Patel','2004-10-12','Spain','5','admin','active' );

INSERT INTO `tmb`.`messages` (`user_id`,`title`,`content`,`created_at`) VALUES 
('1', 'The Healing Power of Forest Bathing', 'Immersing oneself in the serene embrace of a forest, known as forest bathing or shinrin-yoku, offers more than just a scenic retreat. Scientific studies have shown that spending time among trees can lower stress levels, boost immune function, and improve overall well-being. Whether you prefer the towering redwoods of California or the ancient beech forests of Europe, each tree-filled sanctuary provides a therapeutic escape from the bustle of daily life. Share your favorite forest bathing experiences and discover the rejuvenating effects of natures embrace.','2024-07-17 10:15:00'),
('2', 'Urban Jungle: Maximizing Green Spaces in Cities', 'In the concrete jungles of our urban landscapes, trees play a crucial role in creating livable environments. Beyond their aesthetic appeal, urban trees mitigate air pollution, reduce heat island effects, and enhance community well-being. From community tree planting initiatives to innovative rooftop gardens, explore how cities around the world are integrating green spaces into their infrastructure. Join the conversation on sustainable urban development and share your ideas for transforming cities into healthier, more vibrant spaces through strategic tree planting and preservation efforts.','2024-07-18 16:30:45'),
('3', 'Heritage Trees: Guardians of Our Natural History', 'Every tree tells a story, but heritage trees embody a living connection to our past. These majestic giants have witnessed centuries of change and hold cultural significance for communities worldwide. Whether its the ancient baobabs of Africa, the sacred oaks of Europe, or the towering sequoias of North America, heritage trees inspire awe and reverence. Share your encounters with these living monuments, discuss conservation efforts, and celebrate the legacy of heritage trees in preserving our natural and cultural heritage for future generations.','2024-07-19 08:00:20'),
('4', 'Trees and Wildlife: Creating Habitat Havens', 'From the treetops to the forest floor, trees provide essential habitats for a diverse array of wildlife. Birds nest among their branches, squirrels scurry up their trunks, and insects find refuge in their bark. Explore the intricate web of life that depends on trees for survival and discuss conservation strategies to protect these vital ecosystems. Whether you are passionate about birdwatching, biodiversity conservation, or simply enjoy observing natures interactions, share your experiences and insights into the critical role trees play in sustaining wildlife populations worldwide.','2024-07-20 12:45:10'),
('5', 'Climate Change and Trees: Partners in Resilience', 'As our planet faces the challenges of climate change, trees emerge as powerful allies in mitigating its effects. Through carbon sequestration, trees help reduce greenhouse gas concentrations in the atmosphere, while their extensive root systems stabilize soil and prevent erosion. Discuss the role of reforestation initiatives, sustainable forestry practices, and agroforestry in combating climate change and promoting environmental resilience. Share success stories, explore innovative solutions, and advocate for policies that prioritize the protection and restoration of our global forest ecosystems.','2024-07-21 23:59:59')
;

INSERT INTO `tmb`.`replies` (`message_id`,`user_id`,`content`,`created_at`) VALUES 
('1', '2', 'Yeah', '2024-07-17 15:30:00'),
('1', '1', 'nAh', '2024-07-18 09:45:00'),
('2', '3', 'oWZ', '2024-07-19 12:00:00'),
('4', '5', 'Nein', '2024-07-20 17:20:00'),
('1', '5', 'Si', '2024-07-21 20:00:00')
;