import books
import relatedatabase
import configparser


class Support:
    """
    A class working with library directly.
    Contains methods:
    1. __init__(self)
    2. get_book(self)
    3. get_year(self)
    4. get_optional_values(self)
    5. get_genre(self)
    6. load_library(self)
    7. dump_into_library(self)
    8. print_menu(self)
    9. pprint(self, catalogue)
    10. print_authors(self, authors)
    11. menu(self)

    Contains fields:
    1. catalogue - object of Library class
    """

    def __init__(self):
        config = configparser.RawConfigParser()
        config.read("config.cfg")
        module_name = config.get("database", "db_type")
        if module_name == "relatedatabase":
            self.catalogue = relatedatabase.Library()
        else:
            self.catalogue = books.Library()

    def get_book(self):
        """
        Create new dictionary element by using get_xxx functions;
        :return dictionary element that contains book info
        """
        buf = {}
        print("\nEnter new book\n")
        buf['path'] = input("Path: ")
        buf['title'] = input("Title: ")
        buf['author'] = input("Author: ")
        buf['publication'] = input("Publication: ")
        buf['genre'] = self.get_genre()
        buf['description'] = input("Description: ")
        buf['year'] = self.get_year()
        return buf

    @staticmethod
    def get_year():
        """
        Get book year value;
        :returns: None: if year value cannot be converted
                    OR integer value of year
        """
        year = input("Year: ")
        try:
            year = int(year)
        except ValueError:
            return None
        return year

    def get_optional_values(self):
        """
        Get optional values for filtering function;
        if input value of sort order cannot be converted to int turns desc to 0
        else sort order is converted value
        :returns: year_f,year_t: integer values of years
                  desc: sort order
        """
        print("From(optional) ")
        year_f = self.get_year()
        print("To(optional) ")
        year_t = self.get_year()
        try:
            mess = "Sort(optional) : 1 - ascending,  -1 - descending"
            desc = int(input(mess))
        except ValueError:
            desc = 0
        return year_f, year_t, desc

    @staticmethod
    def get_genre():
        """Get genre name

        :returns: None: if genre is not containing
                any symbol or containing only whitespaces
              OR genre name if genre was inputted """
        _genre = input("Genre: ")
        if _genre == '' or _genre.isspace():
            _genre = None
        return _genre

    @staticmethod
    def mod_chosen():
        """
        Choose format of library file
        :returns: 'w' if chosen formats are json or yaml
                or 'wb' if chosen format is pickle
        """
        print('\n Choose format of library(pickle, json, yaml):')
        ch = input()
        if ch == 'json' or ch == 'yaml':
            return 'w'
        elif ch == 'pickle':
            return 'wb'

    def load_library(self):
        """
        Load books from inputted library file
        :return: function load_library from  books module
        """
        file_name = input('\n Enter name of library file:')
        return self.catalogue.load_library(open(file_name, 'rb'))

    def dump_into_library(self):
        """Dump current book catalogue into inputted library file"""
        file_name = input('\n Enter name of library file:')
        try:
            self.catalogue.dump_library(open(file_name, self.mod_chosen()))
        except:
            print("Can`t open file: {:}".format(file_name))

    @staticmethod
    def print_menu():
        """Print simple console menu"""
        print("\nMenu:")
        print("1. Add book to the catalogue")
        print("2. Edit book in the catalogue")
        print("3. Delete book from the catalogue")
        print("4. Filter books")
        print("5. Get authors")
        print("6. Load catalogue from library")
        print("7. Dump catalogue into library")
        print("0. Finish work")

    @staticmethod
    def pprint(catalogue):
        """Prints values of all elements in book catalogue
        :param catalogue: a list of books.
        """
        for i in catalogue:
            print("\nPath: {}, Title: {}".format(i['path'], i['title']))
            print("Author: {}".format(i['author']))
            print("Genre: {}, Year: {}".format(i['genre'], i['year']))
            print("Description: {}\n".format(i['description']))

    @staticmethod
    def print_authors(authors):
        """Prints names of all authors
        :param: authors: a list of authors"""
        for i in authors:
            print("Author: {}".format(i))
