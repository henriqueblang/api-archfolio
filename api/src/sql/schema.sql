CREATE SCHEMA archfolio;

CREATE TABLE archfolio.users (
	id SERIAL PRIMARY KEY,

	username VARCHAR(16) UNIQUE NOT NULL,
	salt BYTEA NOT NULL,
	password BYTEA NOT NULL,

	pfp_url TEXT NULL,

	name VARCHAR(70) NULL,
	description VARCHAR(150) NULL,
	location VARCHAR(50) NULL,

	joined_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE archfolio.followers (
	id SERIAL PRIMARY KEY,

	follower_id INT NOT NULL,
	following_id INT NOT NULL,

	FOREIGN KEY (follower_id) REFERENCES archfolio.users(id) ON DELETE CASCADE,
	FOREIGN KEY (follower_id) REFERENCES archfolio.users(id) ON DELETE CASCADE
);

CREATE TABLE archfolio.posts (
	id SERIAL PRIMARY KEY,
	user_id INT NOT NULL,

	title VARCHAR(20) NULL,
	description VARCHAR(150) NULL,

	tags TEXT[] NULL,
	views INT NOT NULL DEFAULT 0,

	created_at TIMESTAMP NOT NULL DEFAULT NOW(),

	FOREIGN KEY (user_id) REFERENCES archfolio.users(id) ON DELETE CASCADE
);

CREATE TABLE archfolio.metadatas (
	id SERIAL PRIMARY KEY,
	post_id INT NOT NULL,

	is_url BOOLEAN NOT NULL DEFAULT FALSE,
	content TEXT NOT NULL,

	disposition_order INT NOT NULL DEFAULT 0,

	FOREIGN KEY (post_id) REFERENCES archfolio.posts(id) ON DELETE CASCADE
);

CREATE TABLE archfolio.likes (
	id SERIAL PRIMARY KEY,
	user_id INT NOT NULL,
	post_id INT NOT NULL,

	FOREIGN KEY (user_id) REFERENCES archfolio.users(id) ON DELETE CASCADE,
	FOREIGN KEY (post_id) REFERENCES archfolio.posts(id) ON DELETE CASCADE
);

CREATE TABLE archfolio.favorites (
	id SERIAL PRIMARY KEY,
	user_id INT NOT NULL,
	post_id INT NOT NULL,

	FOREIGN KEY (user_id) REFERENCES archfolio.users(id) ON DELETE CASCADE,
	FOREIGN KEY (post_id) REFERENCES archfolio.posts(id) ON DELETE CASCADE
);

CREATE TABLE archfolio.comments (
	id SERIAL PRIMARY KEY,
	user_id INT NOT NULL,
	post_id INT NOT NULL,

	content VARCHAR(1000) NULL,

	created_at TIMESTAMP NOT NULL DEFAULT NOW(),

	FOREIGN KEY (user_id) REFERENCES archfolio.users(id) ON DELETE CASCADE,
	FOREIGN KEY (post_id) REFERENCES archfolio.posts(id) ON DELETE CASCADE
);
