CREATE DATABASE IF NOT EXISTS blog;
USE blog;

CREATE TABLE users(
    id int PRIMARY KEY AUTO_INCREMENT,
    firstname varchar(20) NOT NULL,
    lastname varchar(20) NOT NULL,
    email varchar(30) NOT NULL,
    password varchar(50) NOT NULL,
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