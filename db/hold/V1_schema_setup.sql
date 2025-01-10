# Setup Postgres Schema

DROP SCHEMA IF EXISTS `public`;
CREATE SCHEMA `feedme`;

Create Type `feedme`.`recipe_category` AS ENUM ('breakfast', 'lunch', 'dinner', 'snack', 'dessert', 'drink', 'other');

Create Table `feedme`.`recipes` (
		`id` SERIAL PRIMARY KEY,
		`name` VARCHAR(255) NOT NULL,
		`description` TEXT,
		`ingredients` TEXT,
		`instructions` TEXT,
		`category` RECIPE_CATEGORY,
		`rating` SMALLINT,
		`price_rating` SMALLINT,
		`difficulty_rating` SMALLINT,
		`prep_time_mins` SMALLINT,
		`cook_time_mins` SMALLINT,
		`image` VARCHAR(100),
		`created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
		`updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

Create Table `feedme`.`tags` (
		`id` SERIAL PRIMARY KEY,
		`name` VARCHAR(255) NOT NULL,
		`created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
);

Create Table `feedme`.`recipe_tags` (
		`recipe_id` INT,
		`tag_id` INT,
		PRIMARY KEY (`recipe_id`, `tag_id`),
		FOREIGN KEY (`recipe_id`) REFERENCES `feedme`.`recipes`(`id`),
		FOREIGN KEY (`tag_id`) REFERENCES `feedme`.`tags`(`id`)
);
