DROP TABLE if exists posts;
CREATE TABLE posts
(
id SERIAL PRIMARY KEY,
title TEXT NOT NULL,
post_date TEXT NOT NULL,
description TEXT NOT NULL,
html_file TEXT NOT NULL
);