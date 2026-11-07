CREATE DATABASE IF NOT EXISTS blog;
USE blog;

CREATE TABLE users(
    id int PRIMARY KEY AUTO_INCREMENT,
    firstname varchar(20) NOT NULL,
    lastname varchar(20) NOT NULL,
    email varchar(30) NOT NULL,
    password varchar(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    verified_at TIMESTAMP NULL,
    reset_token varchar(50) NULL,
    reset_expires_at TIMESTAMP NULL
);

CREATE TABLE posts(
    id int PRIMARY KEY AUTO_INCREMENT,
    user_id int NOT NULL,
    CONSTRAINT fk_post_user_id FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
    image_url varchar(255) NULL,
    title varchar(100) NOT NULL,
    content text NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE comments(
    id int PRIMARY KEY AUTO_INCREMENT,
    user_id int NOT NULL,
    CONSTRAINT fk_comment_user_id FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
    post_id int NOT NULL,
    CONSTRAINT fk_comment_post_id FOREIGN KEY(post_id) REFERENCES posts(id) ON DELETE CASCADE,
    content text NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

INSERT INTO `users` (`id`, `firstname`, `lastname`, `email`, `password`, `created_at`, `updated_at`, `verified_at`, `reset_token`, `reset_expires_at`) VALUES
(1,	'Admin',	'Admin',	'admin@email.com',	'$2b$12$YmTY8NQBwXZjjE7Z8XiKUOY94cM5rFMq5pJwywzOrwoPRXPOCLv8u',	'2026-11-06 18:13:06',	'2026-11-07 01:28:33',	NULL,	NULL,	NULL),
(2,	'Normal',	'User',	'normal.user@email.com',	'$2b$12$YmTY8NQBwXZjjE7Z8XiKUOY94cM5rFMq5pJwywzOrwoPRXPOCLv8u',	'2026-11-06 18:13:27',	'2026-11-07 01:28:46',	NULL,	NULL,	NULL),
(3,	'test',	'user',	'test.user@email.com',	'$2b$12$YmTY8NQBwXZjjE7Z8XiKUOY94cM5rFMq5pJwywzOrwoPRXPOCLv8u',	'2026-11-07 01:23:38',	'2026-11-07 01:28:19',	NULL,	NULL,	NULL);

INSERT INTO `posts` (`id`, `user_id`, `image_url`, `title`, `content`, `created_at`, `updated_at`) VALUES
(1,	1,	NULL,	'First Post',	'Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex sapien vitae pellentesque sem placerat. In id cursus mi pretium tellus duis convallis. Tempus leo eu aenean sed diam urna tempor. Pulvinar vivamus fringilla lacus nec metus bibendum egestas. Iaculis massa nisl malesuada lacinia integer nunc posuere. Ut hendrerit semper vel class aptent taciti sociosqu. Ad litora torquent per conubia nostra inceptos himenaeos.\r\n\r\nLorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex sapien vitae pellentesque sem placerat. In id cursus mi pretium tellus duis convallis. Tempus leo eu aenean sed diam urna tempor. Pulvinar vivamus fringilla lacus nec metus bibendum egestas. Iaculis massa nisl malesuada lacinia integer nunc posuere. Ut hendrerit semper vel class aptent taciti sociosqu. Ad litora torquent per conubia nostra inceptos himenaeos.\r\n\r\nLorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex sapien vitae pellentesque sem placerat. In id cursus mi pretium tellus duis convallis. Tempus leo eu aenean sed diam urna tempor. Pulvinar vivamus fringilla lacus nec metus bibendum egestas. Iaculis massa nisl malesuada lacinia integer nunc posuere. Ut hendrerit semper vel class aptent taciti sociosqu. Ad litora torquent per conubia nostra inceptos himenaeos.\r\n\r\nLorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex sapien vitae pellentesque sem placerat. In id cursus mi pretium tellus duis convallis. Tempus leo eu aenean sed diam urna tempor. Pulvinar vivamus fringilla lacus nec metus bibendum egestas. Iaculis massa nisl malesuada lacinia integer nunc posuere. Ut hendrerit semper vel class aptent taciti sociosqu. Ad litora torquent per conubia nostra inceptos himenaeos.\r\n\r\nLorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex sapien vitae pellentesque sem placerat. In id cursus mi pretium tellus duis convallis. Tempus leo eu aenean sed diam urna tempor. Pulvinar vivamus fringilla lacus nec metus bibendum egestas. Iaculis massa nisl malesuada lacinia integer nunc posuere. Ut hendrerit semper vel class aptent taciti sociosqu. Ad litora torquent per conubia nostra inceptos himenaeos.',	'2026-11-06 18:31:15',	'2026-11-06 18:31:15'),
(2,	1,	NULL,	'Second Post',	'Lorem ipsum dolor sit amet consectetur adipiscing elit. Consectetur adipiscing elit quisque faucibus ex sapien vitae. Ex sapien vitae pellentesque sem placerat in id. Placerat in id cursus mi pretium tellus duis. Pretium tellus duis convallis tempus leo eu aenean.',	'2026-11-06 18:33:33',	'2026-11-06 18:33:33');

INSERT INTO `comments` (`id`, `user_id`, `post_id`, `content`, `created_at`, `updated_at`) VALUES
(1,	1,	1,	'First comment',	'2026-11-06 18:33:51',	'2026-11-06 18:33:51'),
(2,	1,	1,	'Second Comment',	'2026-11-06 18:34:00',	'2026-11-06 18:34:00');
