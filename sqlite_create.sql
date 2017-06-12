CREATE TABLE lib (
	id integer PRIMARY KEY AUTOINCREMENT,
	book integer,
	author integer
);

CREATE TABLE book (
	id integer PRIMARY KEY AUTOINCREMENT,
	title varchar,
	description varchar,
	genre varchar,
	year integer,
	path varchar
);

CREATE TABLE author (
	id integer PRIMARY KEY AUTOINCREMENT,
	author varchar
);

