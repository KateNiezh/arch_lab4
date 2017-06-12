CREATE TABLE "lib" (
	"id" serial(10) NOT NULL,
	"book" integer(10) NOT NULL,
	"author" integer(10) NOT NULL,
	CONSTRAINT lib_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "book" (
	"id" serial(10) NOT NULL,
	"title" varchar(100) NOT NULL,
	"description" varchar(100) NOT NULL,
	"genre" varchar(100) NOT NULL,
	"year" integer(10) NOT NULL,
	"path" varchar(100) NOT NULL,
	CONSTRAINT book_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



CREATE TABLE "author" (
	"id" serial(10) NOT NULL,
	"author" varchar(100) NOT NULL,
	CONSTRAINT author_pk PRIMARY KEY ("id")
) WITH (
  OIDS=FALSE
);



ALTER TABLE "lib" ADD CONSTRAINT "lib_fk0" FOREIGN KEY ("book") REFERENCES "book"("id");
ALTER TABLE "lib" ADD CONSTRAINT "lib_fk1" FOREIGN KEY ("author") REFERENCES "author"("id");



