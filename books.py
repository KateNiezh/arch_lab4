class Library:
    """
    A class working with library directly.

    Contents methods:
    1. __init__(self)
    2. add_book(self, new)
    3. search_book(self, title, author)
    4. edit_book(self, old_title, old_author, new)
    5. delete_book(self, title, author)
    6. filter_books(self, key, value, year_from=None, year_to=None, desc=0)
    7. get_authors(self, genre=None)
    8. get_config(filename, section, option)
    9. set_config(filename, section, option, new_value)
    10. load_library(self, file, test_mode=False)
    11. dump_library(self, file)

    Contents list:
    1. library
    """

    def __init__(self):
        self.library = []

    def add_book(self, new):
        """
        Adds new book to self.library.
        :param new: a dictionary with such keys: 'path', 'title', 'author',
        'publication', 'genre', 'description', 'year'.
        :returns 1 if the book is already in catalogue, or 0 otherwise.
        """
        if new in self.library:
            return 1
        self.library.append(new)
        return 0

    def search_book(self, title, author):
        """
        Searches a book in self.library.
        :param title: a string - title of the book, which is searched.
        :param author: a string - name of author of the book, which is
        searched.
        :returns a dictionary, corresponding to searched book, or nothing, if
        book is not found.
        """
        for x in self.library:
            if (x["title"] == title) and (x["author"] == author):
                return x

    def edit_book(self, old_title, old_author, new):
        """
        Edits a book in self.library.
        :param old_title: a string - title of the book, which will be edited.
        :param old_author: a string - author of the book, which will be
        edited.
        :param new: a dictionary, containing new information about the book;
        must have keys: 'path', 'title', 'author', 'publication', 'genre',
        'description', 'year'.
        :returns new book in case of success, or nothing, if old book is not
        found in self.library.
        """
        book = self.search_book(old_title, old_author)
        if book:
            i = self.library.index(book)
            self.library.remove(book)
            self.library.insert(i, new)
            return new

    def delete_book(self, title, author):
        """
        Removes a book from self.library.
        :param title: a string - title of the book, which will be deleted.
        :param author: a string - author of the book, which will be deleted.
        :returns 0 in case of success, or 1, if the book is not found in
        self.library.
        """
        try:
            self.library.remove(self.search_book(title, author))
            return 0
        except ValueError:
            return 1

    @staticmethod
    def __sort_by_year(book_list, desc):
        if desc == 1:
            return sorted(book_list, key=lambda x: x["year"])
        if desc == -1:
            return sorted(book_list, key=lambda x: x["year"], reverse=True)
        return book_list

    def __filter_by_year(self, book_list, year_from, year_to, desc):
        if year_from is None:
            return self.__sort_by_year(book_list, desc)
        if year_to is None:
            year_to = year_from
        res = []
        for x in book_list:
            if (x["year"] in range(year_from, year_to+1)) and (x not in res):
                res.append(x)
        return self.__sort_by_year(res, desc)

    def filter_books(self, key, value, year_from=None, year_to=None, desc=0):
        """
        Filters self.library by the key and/or publishing year and sorts it.
        :param key: "genre", "author", or "year".
        :param value: a string - genre's name, if key="genre"; a string -
        author's name, if key="author"; if key="year", any value is allowed.
        :param year_from: an integer, lower limit of publishing years'
        diapason; if year_from=None, filtering by year is not performed.
        :param year_to: an integer, higher limit of publishing year's
        diapason; if year_to=None and year_from is not None, searches only
        books, published in year_from; if year_from=None, any year_to is
        allowed.
        :param desc: if 1, sorts selected books by publishing year increasing,
        if -1 - by publishing year decreasing; otherwise sorting is not
        performed.
        :returns a filtered and sorted list of books.
        """
        if key not in ["author", "genre", "year"]:
            return
        if key == "year":
            return self.__filter_by_year(self.library, year_from,
                                         year_to, desc)
        res = []
        for x in self.library:
            if (x[key] == value) and (x not in res):
                res.append(x)
        return self.__filter_by_year(res, year_from, year_to, desc)

    def get_authors(self, genre=None):
        """
        Selects authors, whose books relate to genre.
        :param genre: a string - name of the genre, authors must relate to;
        if None, returns all of the authors in self.library.
        :returns list of strings - authors' names.
        """
        authors = []
        for x in self.library:
            if (x["genre"] == genre) and (x["author"] not in authors):
                authors.append(x["author"])
                continue
            if (genre is None) and (x["author"] not in authors):
                authors.append(x["author"])
        return authors

    @staticmethod
    def get_config(filename, section, option):
        """
        Parses .cfg file and gets some value from it.
        :param filename: a string - file name.
        :param section: a string - name of section.
        :param option: a string - name of option.
        :returns value of option in section in case of success, or nothing
        otherwise.
        """
        import configparser
        config = configparser.RawConfigParser()
        config.read(filename)
        return config.get(section, option)

    @staticmethod
    def set_config(filename, section, option, new_value):
        """
        Parses .cfg file and sets new value for some option.
        :param filename: a string - file name.
        :param section: a string - name of section.
        :param option: a string - name of option.
        :param new_value: a new value of option in section.
        :returns new_value in case of success, or nothing otherwise.
        """
        import configparser
        config = configparser.RawConfigParser()
        config.read(filename)
        config.set(section, option, new_value)
        with open(filename, "w") as configfile:
            config.write(configfile)
        return new_value

    @staticmethod
    def __import_db_module(file_type):
        if file_type == "pkl":
            import db_pickle
            return db_pickle
        elif file_type == "json":
            import db_json
            return db_json
        elif file_type == "yaml":
            import db_yaml
            return db_yaml

    def load_library(self, file):
        """
        Loads to self.library a book list from .pkl, .json or .yaml file.
        :param file: a file object; file must be opened in "rb" mode, and be
        the same type, as set in 'db_file_type' option in 'config.cfg'.
        :returns 0 in case of success.
        """
        file_type = self.get_config("config.cfg", "storage", "db_file_type")
        db = self.__import_db_module(file_type)
        self.library = db.DataBase.load_library(file)
        return 0

    def dump_library(self, file):
        """
        Dumps self.library into .pkl, .json or .yaml file.
        :param file: a file object; file must be opened in "wb" mode, if it is
        .pkl, or in "w" mode if it is .json or .yaml; file type must be the
        same, as set in 'db_file_type' option in 'config.cfg'.
        :returns catalogue in case of success.
        """
        file_type = self.get_config("config.cfg", "storage", "db_file_type")
        db = self.__import_db_module(file_type)
        return db.DataBase.dump_library(file, self.library)
