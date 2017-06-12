import pymysql.cursors
import sqlite3
import psycopg2
import configparser


class Library:
    """
    class for working with relate database (mysql, postgres, sqlite).
    """
    def __init__(self):
        """
        constructor. init db manager (mysql, postgres, sqlite).
        Take configs from config.cfg 
        """
        config = configparser.RawConfigParser()
        config.read("config.cfg")
        dbname = config.get("storage", "db_file_type")
        self.db = None
        if dbname == "Mysql":
            self.db = Mysql()
        elif dbname == "Postgres":
            self.db = Postgres()
        elif dbname == "Sqlite":
            self.db = Sqlite()

    def add_book(self, new):
        """
        add new book to database        
        """
        bookid = self.db.insert("book", {
            "title": new["title"], "description": new["description"],
            "genre": new["genre"], "year": new["year"], "path": new["path"]})
        authorid = self.db.insert("author", {"author": new["author"]})
        return self.db.insert("lib", {"book": bookid, "author": authorid})

    def search_book(self, title, author):
        """
        search book by title and author        
        """
        return self.db.find(title, author)

    def edit_book(self, old_title, old_author, new):
        """
        edit book with old_title and old_author to new data 
        """
        self.db.update(
            "book", {
                "title": new["title"],
                "description": new["description"],
                "genre": new["genre"],
                "year": new["year"],
                "path": new["path"]
            }, "title", old_title)
        self.db.insert(
            "author", {"author": new["author"]}, "author", old_author)
        return True

    def delete_book(self, title, author):
        """
        delete book of author :author from database with title :title
        """
        return self.db.delete("book", author, title)

    def filter_books(self, key, value, year_from=None, year_to=None, desc=0):
        """
        filter books where genre, year, author (key) == value,
        from year year_from to year_to, order asc/desc
        """
        key = "book." + key if key in ["year", "genre"] else "author." + key
        return self.db.filter(key, value, year_from, year_to, desc)

    def get_authors(self, genre=None):
        """
        get list of authors (if genre != None -- of current genre)
        """
        return [i["author"] for i in self.db.selectAuthors(genre)]

    def load_library(self, var):
        pass

    def dump_library(self, var):
        pass


class Mysql:
    """
    class for creating and executing queries to MySQL
    """
    def __init__(self):
        """
        connect o MySQL server and database
        """
        self.connector = pymysql.connect(
            host="localhost",
            user="root",
            passwd="1111",
            db="library",
            cursorclass=pymysql.cursors.DictCursor)

    def insert(self, table, data):
        """
        add new book to DB
        """
        self.connector.begin()
        with self.connector.cursor() as cursor:
            cursor.execute(
                'insert into %s (%s) values (%s)' %
                (table, ', '.join(data.keys()),
                 ', '.join(["%s"] * len(data.keys()))),
                list(data.values()))
            self.connector.commit()
        return cursor.lastrowid

    def selectAuthors(self, genre):
        """
        get all authors (or authors of genre)
        """
        genre = "" if genre is None else " and book.genre = " + genre
        sql = "SELECT author.author as author FROM lib, book, author WHERE " \
              "lib.book = book.id AND lib.author = author.id" + genre
        with self.connector.cursor() as cursor:
            cursor.execute(sql)
            res = cursor.fetchall()
        return res

    def find(self, title, author):
        """
        find book with :title of author :author
        """
        sql = "select * from book, author, lib where " \
              "book.title = '%s' and author.author = '%s' and " \
              "lib.book = book.id and lib.author = author.id" % (title, author)
        with self.connector.cursor() as cursor:
            cursor.execute(sql)
            res = cursor.fetchall()
        return res

    def filter(self, key, value, year_from, year_to, desc):
        """
        filter books where genre, year, author (key) == value,
        from year year_from to year_to, order asc/desc
        """
        desc = "desc" if desc == -1 else "asc"
        sql = "select * from lib, book, author where %s = '%s' and" \
              " book.year > '%s' and book.year < '%s' and " \
              "lib.book = book.id and lib.author = author.id "\
              "order by book.year %s" % \
              (key, value, year_from, year_to, desc)
        with self.connector.cursor() as cursor:
            cursor.execute(sql)
            res = cursor.fetchall()
        return res

    def update(self, table, data, key, value):
        """
        update book in DB with new data, where old_row[key] == value
        """
        upd = ",".join(['`%s`=\'%s\'' % (k, v) for (k, v) in data.items()])
        sql = "update " + table + "set " + upd[:-1]
        self.connector.begin()
        with self.connector.cursor() as cursor:
            cursor.execute(sql + " where `" + key + "`='" + value + "'")
            self.connector.commit()
        return cursor.rowcount

    def delete(self, table, author, title):
        """
        remove book from DB by author_name and title_name
        """
        self.connector.begin()
        with self.connector.cursor() as cursor:
            cursor.execute(
                "delete from " + table + " where `author`='" + author +
                "' and `title`='" + title + "'")
            self.connector.commit()
        return cursor.rowcount


class Sqlite:
    """
    class for creating and executing queries to Sqlite
    """
    def __init__(self):
        """
        connect to Sqlite DB
        """
        self.connector = sqlite3.connect('./library')
        self.connector.row_factory = Sqlite.dict_factory

    def insert(self, table, data):
        """
        add new book to DB
        """
        cursor = self.connector.cursor()
        cursor.execute(
            'insert into %s (%s) values (%s)' %
            (table, ', '.join(data.keys()),
             ', '.join(["%s"] * len(data.keys()))),
            list(data.keys()))
        self.connector.commit()
        return cursor.lastrowid

    def selectAuthors(self, genre):
        """
        get all authors (or authors of genre)
        """
        genre = "" if genre is None else " and book.genre = " + genre
        sql = "SELECT author.author as author FROM lib, book, author WHERE " \
              "lib.book = book.id AND lib.author = author.id" + genre
        cursor = self.connector.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def find(self, title, author):
        """
        find book with :title of author :author
        """
        sql = "select * from book, author, lib where " \
              "book.title = '%s' and author.author = '%s' and " \
              "lib.book = book.id and lib.author = author.id" % (title, author)
        cursor = self.connector.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def filter(self, key, value, year_from, year_to, desc):
        """
        filter books where genre, year, author (key) == value,
        from year year_from to year_to, order asc/desc
        """
        desc = "desc" if desc == -1 else "asc"
        sql = "select * from lib, book, author where %s = '%s' and" \
              " book.year > '%s' and book.year < '%s' and " \
              "lib.book = book.id and lib.author = author.id "\
              "order by book.year %s" % \
              (key, value, year_from, year_to, desc)
        cursor = self.connector.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def update(self, table, data, key, value):
        """
        update book in DB with new data, where old_row[key] == value
        """
        pass
        upd = ",".join(['`%s`=\'%s\'' % (k, v) for (k, v) in data.items()])
        sql = "update " + table + "set " + upd[:-1]
        cursor = self.connector.cursor()
        cursor.execute(sql + " where `" + key + "`='" + value + "'")
        self.connector.commit()
        return cursor.rowcount

    def delete(self, table, author, title):
        """
        remove book of author_name :author with title :title from Sqlite DB
        """
        cursor = self.connector.cursor()
        cursor.execute(
            "delete from " + table + " where title = '" + title + "'")
        self.connector.commit()
        return cursor.rowcount

    @staticmethod
    def dict_factory(cursor, row):
        """
        method for converting result of base list cursor to dictionary
        """
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d


class Postgres:
    """
    class for creating and executing queries to PostgreSQL
    """
    def __init__(self):
        """
        connect to postgres DB
        """
        self.connector = psycopg2.connect(
            dbname='library',
            user='postgres',
            password='1111',
            cursor_factory=psycopg2.extras.RealDictCursor)

    def insert(self, table, data):
        """
        add new book to DB
        """
        with self.connector.cursor() as cursor:
            cursor.execute(
                'insert into %s (%s) values (%s)' %
                (table, ', '.join(data.keys()),
                 ', '.join(["%s"] * len(data.keys()))) +
                " returning id", list(data.values()))
            res = cursor.fetchone()['id']
        self.connector.commit()
        return res

    def selectAuthors(self, genre):
        """
        get all authors (or authors of genre)
        """
        genre = "" if genre is None else " and book.genre = " + genre
        sql = "SELECT author.author as author FROM lib, book, author WHERE " \
              "lib.book = book.id AND lib.author = author.id" + genre
        with self.connector.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

    def find(self, title, author):
        """
        find book with :title of author :author
        """
        sql = "select * from book, author, lib where " \
              "book.title = '%s' and author.author = '%s' and " \
              "lib.book = book.id and lib.author = author.id" % (title, author)
        with self.connector.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

    def filter(self, key, value, year_from, year_to, desc):
        """
        filter books where genre, year, author (key) == value,
        from year year_from to year_to, order asc/desc
        """
        desc = "desc" if desc == -1 else "asc"
        sql = "select * from lib, book, author where %s = '%s' and" \
              " book.year > '%s' and book.year < '%s' and " \
              "lib.book = book.id and lib.author = author.id "\
              "order by book.year %s" % \
              (key, value, year_from, year_to, desc)
        with self.connector.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

    def update(self, table, data, key, value):
        """
        update book in DB with new data, where old_row[key] == value
        """
        upd = ",".join(['`%s`=\'%s\'' % (k, v) for (k, v) in data.items()])
        sql = "update " + table + "set " + upd[:-1]
        with self.connector.cursor() as cursor:
            cursor.execute(sql + " where `" + key + "`='" + value + "'")
            res = cursor.rowcount
        self.connector.commit()
        return res

    def delete(self, table, author, title):
        """
        remove book from DB by author_name and title_name
        """
        with self.connector.cursor() as cursor:
            cursor.execute(
                "delete from " + table + " where title = '" + title + "'")
            res = cursor.rowcount
        self.connector.commit()
        return res
