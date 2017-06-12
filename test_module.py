import io
import unittest
import pickle
import json
import yaml
import books
book_list = [{"path": "Path", "title": "T1", "author": "A1",
              "publication": "P", "genre": "G", "description": "D",
              "year": 1900},
             {"path": "Path", "title": "T2", "author": "A2",
              "publication": "P", "genre": "G", "description": "D",
              "year": 2000},
             {"path": "Path", "title": "T3", "author": "A2",
              "publication": "P", "genre": "G", "description": "D",
              "year": 2010}]


class TestPickle(unittest.TestCase):

    def test_load_library(self):
        lib = books.Library()
        file = io.BytesIO(pickle.dumps(book_list))
        lib.set_config("config.cfg", "storage", "db_file_type", "pkl")
        lib.load_library(file)
        self.assertEqual(book_list, lib.library)

    def test_dump_library(self):
        lib = books.Library()
        file = io.BytesIO()
        for book in book_list:
            lib.add_book(book)
        lib.set_config("config.cfg", "storage", "db_file_type", "pkl")
        self.assertEqual(book_list, lib.dump_library(file))


class TestJson(unittest.TestCase):

    def test_load_library(self):
        lib = books.Library()
        file = io.StringIO(json.dumps(book_list))
        lib.set_config("config.cfg", "storage", "db_file_type", "json")
        lib.load_library(file)
        self.assertEqual(book_list, lib.library)

    def test_dump_library(self):
        lib = books.Library()
        file = io.StringIO()
        for book in book_list:
            lib.add_book(book)
        lib.set_config("config.cfg", "storage", "db_file_type", "json")
        self.assertEqual(book_list, lib.dump_library(file))


class TestYaml(unittest.TestCase):

    def test_load_library(self):
        lib = books.Library()
        file = io.StringIO(yaml.dump(book_list))
        lib.set_config("config.cfg", "storage", "db_file_type", "yaml")
        lib.load_library(file)
        self.assertEqual(book_list, lib.library)

    def test_dump_library(self):
        lib = books.Library()
        file = io.StringIO()
        for book in book_list:
            lib.add_book(book)
        lib.set_config("config.cfg", "storage", "db_file_type", "yaml")
        self.assertEqual(book_list, lib.dump_library(file))


class TestBooks(unittest.TestCase):

    def test_add_book(self):
        lib = books.Library()
        book = book_list[2]
        self.assertEqual(0, lib.add_book(book))
        self.assertEqual(1, lib.add_book(book))

    def test_search_book(self):
        lib = books.Library()
        book = book_list[2]
        lib.add_book(book)
        self.assertEqual(book, lib.search_book("T3", "A2"))
        self.assertEqual(None, lib.search_book("TT", "AA"))

    def test_edit_book(self):
        lib = books.Library()
        book = book_list[1]
        new = book_list[2]
        lib.add_book(book)
        self.assertEqual(new, lib.edit_book("T2", "A2", new))
        self.assertEqual(None, lib.edit_book("Tit", "A", new))

    def test_delete_book(self):
        lib = books.Library()
        book = book_list[2]
        lib.add_book(book)
        self.assertEqual(0, lib.delete_book("T3", "A2"))
        self.assertEqual(1, lib.delete_book("T3", "A2"))

    def test_filter_books(self):
        lib = books.Library()
        lib.add_book(book_list[1])
        lib.add_book(book_list[0])
        lib.add_book(book_list[2])
        # Get all of the books:
        self.assertEqual([book_list[1], book_list[0], book_list[2]],
                         lib.filter_books("year", None))
        # Get books, published in only one year, without sorting:
        self.assertEqual([book_list[1]],
                         lib.filter_books("year", "anything", 2000))
        # Get books, published between two years, by year decreasing:
        self.assertEqual([book_list[2], book_list[1]],
                         lib.filter_books("year", None, 2000, 2010, -1))
        # Get books, published between two years, by year increasing:
        self.assertEqual([book_list[0], book_list[1], book_list[2]],
                         lib.filter_books("year", None, 1900, 2100, 1))
        # Get books of one author from all years, by years decreasing:
        self.assertEqual([book_list[2], book_list[1]],
                         lib.filter_books("author", "A2", None, None, -1))
        # Get books of one author from one year, without sorting:
        self.assertEqual([book_list[1]],
                         lib.filter_books("author", "A2", 2000))
        # Get books of one author between two years, by increasing:
        self.assertEqual([book_list[1]],
                         lib.filter_books("author", "A2", 2000, 2005, 1))
        # Books of one genre from all years, by years increasing:
        self.assertEqual([book_list[0], book_list[1], book_list[2]],
                         lib.filter_books("genre", "G", None, None, 1))
        # Books of one genre from one year, without sorting:
        self.assertEqual([book_list[1]],
                         lib.filter_books("genre", "G", 2000))
        # Books of one genre between two years, by decreasing:
        self.assertEqual([book_list[2], book_list[1]],
                         lib.filter_books("genre", "G", 2000, 2015, -1))
        # Wrong test
        self.assertEqual(None, lib.filter_books("wrong", "something"))

    def test_get_authors(self):
        lib = books.Library()
        lib.add_book({"path": "Path", "title": "T2", "author": "A2",
                      "publication": "P", "genre": "G1", "description": "D",
                      "year": 2000})
        lib.add_book({"path": "Path", "title": "T1", "author": "A1",
                      "publication": "P", "genre": "G1", "description": "D",
                      "year": 1900})
        lib.add_book({"path": "Path", "title": "T3", "author": "A2",
                      "publication": "P", "genre": "G2", "description": "D",
                      "year": 2010})
        self.assertEqual(['A2'], lib.get_authors("G2"))
        self.assertEqual(['A2', 'A1'], lib.get_authors())


if __name__ == '__main__':
    unittest.main()
