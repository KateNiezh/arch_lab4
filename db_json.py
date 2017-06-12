import json


class DataBase:
    """
    A class to work with .json files.
    Contents methods:
    1. load_library(file)
    2. dump_library(file)
    """

    @staticmethod
    def load_library(file):
        """
        Loads library from .json file.
        :param file: file object.
        :returns a list of books in case of success.
        """
        with file:
            res = json.loads(file.read())
        return res

    @staticmethod
    def dump_library(file, catalogue):
        """
        Dumps library into .json file.
        :param file: file object.
        :param catalogue: a list of books.
        :returns catalogue in case of success.
        """
        with file:
            json.dump(catalogue, file)
        return catalogue
