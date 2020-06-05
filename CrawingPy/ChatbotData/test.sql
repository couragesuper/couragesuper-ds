create table `tDlgTest` (
  `sentID` int(10) NOT NULL AUTO_INCREMENT,
  `sentence` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `reply` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`sentID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

select * from tDlgTest;

INSERT INTO chatbot.tKomoDict
(word, morph) 
VALUES ('자연어 처리', 'NN');

INSERT INTO chatbot.tKomoDict
(word, morph) 
VALUES ('인공지능', 'NN');

