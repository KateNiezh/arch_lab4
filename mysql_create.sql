CREATE TABLE `lib` (
	`id` INT(10) NOT NULL AUTO_INCREMENT,
	`book` INT(10) NOT NULL,
	`author` INT(10) NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `book` (
	`id` INT(10) NOT NULL AUTO_INCREMENT,
	`title` varchar(100) NOT NULL,
	`description` varchar(100) NOT NULL,
	`genre` varchar(100) NOT NULL,
	`year` INT(10) NOT NULL,
	`path` varchar(100) NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `author` (
	`id` INT(10) NOT NULL AUTO_INCREMENT,
	`author` varchar(100) NOT NULL,
	PRIMARY KEY (`id`)
);

ALTER TABLE `lib` ADD CONSTRAINT `lib_fk0` FOREIGN KEY (`book`) REFERENCES `book`(`id`);

ALTER TABLE `lib` ADD CONSTRAINT `lib_fk1` FOREIGN KEY (`author`) REFERENCES `author`(`id`);

