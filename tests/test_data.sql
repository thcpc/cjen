CREATE DATABASE IF NOT EXISTS `cjen_test_sql`;

USE `cjen_test_sql`;

DROP TABLE IF EXISTS `company`;

CREATE TABLE `company` (
`id` int NOT NULL AUTO_INCREMENT,
`name` varchar(300) DEFAULT NULL,
PRIMARY KEY (`id`)
);

LOCK TABLES `company` WRITE;
INSERT INTO `company` VALUES (1,"C01");
INSERT INTO `company` VALUES (2,"C02");
INSERT INTO `company` VALUES (3,"C03");
INSERT INTO `company` VALUES (4,"C04");
INSERT INTO `company` VALUES (5,"C05");
UNLOCK TABLES;

CREATE TABLE `employees` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(300) DEFAULT NULL,
  `company_id` int not null,
  PRIMARY KEY (`id`)
);

LOCK TABLES `employees` WRITE;
INSERT INTO `employees` VALUES (1,"E01",1);
INSERT INTO `employees` VALUES (2,"E02",1);
INSERT INTO `employees` VALUES (3,"E03",1);
INSERT INTO `employees` VALUES (4,"E04",1);
INSERT INTO `employees` VALUES (5,"E05",1);
INSERT INTO `employees` VALUES (6,"E06",1);
INSERT INTO `employees` VALUES (7,"E07",1);
INSERT INTO `employees` VALUES (8,"E08",2);
INSERT INTO `employees` VALUES (9,"E09",2);
INSERT INTO `employees` VALUES (10,"E10",5);
INSERT INTO `employees` VALUES (11,"E11",5);
INSERT INTO `employees` VALUES (12,"E12",5);
INSERT INTO `employees` VALUES (13,"E13",5);
INSERT INTO `employees` VALUES (14,"E14",5);
INSERT INTO `employees` VALUES (15,"E15",5);
UNLOCK TABLES;