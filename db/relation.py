from btree.Btree import *
from .errors import *
import os


class Tuple:
    def __init__(self, primary_key, attributes):
        self._data = {}
        self._primary_key = primary_key
        self._attributes = attributes

    def get_primary_key(self):
        return self._primary_key

    def __lt__(self, other):
        return self._primary_key < other.get_primary_key()

    def __le__(self, other):
        return self._primary_key <= other.get_primary_key()
    # def  __eq__(self, other):
    #
    # def  __ne__(self, other):

    def __gt__(self, other):
        return self._primary_key > other.get_primary_key()

    def __ge__(self, other):
        return self._primary_key >= other.get_primary_key()

    def __str__(self):
        return "(PK: " + str(self._primary_key) + ")"


class Relation:
    def __init__(self, schema):
        # self._data = Btree(5)
        self._data = {}
        self._primary_key = schema['primary_key']
        self._attributes = schema['attributes']
        self._location = schema['location']

        self._load_file()

    def _load_file(self):
        if os.path.isfile(self._location):
            print("load file")

    # def __init__(self, primary_key, attributes):
    #     self._data = Btree(5)
    #     self._primary_key = primary_key
    #     self._attributes = attributes

    def _insert_to_file(self, attributes):
        if os.path.isfile(self._location):
            print("update file")
        else:
            print("None")

    def insert_values(self, attributes):
        primary_key = ""

        for abute in attributes:
            if abute['attribute'] == self._primary_key:
                primary_key = abute['value']

        if primary_key == "":
            raise Error

        new_tuple = Tuple(primary_key, attributes)
        self._data[primary_key] = new_tuple
        print(self._data)
        # self._data.insert(new_tuple)
        # self._data.print_tree()


