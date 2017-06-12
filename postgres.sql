create table book(
	id serial not null
		constraint book_pk
			primary key,
	title varchar(100) not null,
	description varchar(100) not null,
	genre varchar(100) not null,
	year integer not null,
	path varchar(100) not null
);

create table author(
	id serial not null
		constraint author_pk
			primary key,
	author varchar(100) not null
);

create table lib(
	id serial not null
		constraint lib_pk
			primary key,
	book integer not null
		constraint book-fk
			references book
				on update cascade on delete cascade,
	author integer not null
		constraint author-fk
			references author
				on update cascade on delete cascade
);

create index "fki_book-fk"
	on lib (book);

create index "fki_author-fk"
	on lib (author);

