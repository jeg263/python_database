from .errors import *
import os
import arff
import sys
import fileinput


class IndexSet:
    def __init__(self, start_index):
        self._data = {}
        self.relation = start_index.relation
        self.add_index(start_index)

    def add_sub_index(self, sub_index):
        for k,v in self._data.items():
            v.add_sub_index(sub_index)

    def add_index(self, index):
        if index.attribute not in self._data.keys():
            self._data[index.attribute] = index

    def get_index_attributes(self):
        return self._data.keys()

    def find_index(self, attribute):
        if attribute not in self._data.keys():
            return None
        return self._data[attribute]


class Index:
    def __init__(self, name, relation, attribute, master_index=False):
        self.name = name
        self.relation = relation
        self.attribute = attribute
        self._data = {}
        self._master_index = master_index
        self._sub_index = None

        if master_index:
            self._location = "./index/" + name + ".csv"
            self._load_index()

    def update_attribute_name(self, new_name):
        self.attribute = new_name

    def add_sub_index(self, sub_index):
        if self._sub_index:
            self._sub_index.add_sub_index(sub_index)
        else:
            self._sub_index = sub_index

    def find(self, key):
        index_data = []
        if key in self._data.keys():
            index_data = self._data[key]

        if self._sub_index:
            final_index_data = []
            for key in index_data:
                final_index_data += self._sub_index.find(key)
            return final_index_data
        return index_data

    def _load_index(self):
        if os.path.isfile(self._location):
            with open(self._location) as inf:
                for line in inf:
                    new_things = line.rstrip().split(',')
                    key = new_things.pop(0)
                    self._data[key] = new_things
            inf.close()

    def add_index(self, key, loc):
        if self._master_index:
            self._add_index_from_file(key, loc)
        else:
            if str(key) in self._data.keys():
                current_locations = self._data[key]
                current_locations.append(loc)
                self._data[key] = current_locations
            else:
                self._data[key] = [loc]

    def _add_index_from_file(self, key, loc):
        self._load_index()

        index_data = []

        all_indexes = []

        if os.path.isfile(self._location):
            with open(self._location) as inf:
                for line in inf:
                    all_indexes.append(line.rstrip().split(','))
            inf.close()

        index_data.append([str(key), str(loc)])

        print_end = True
        f = open(self._location, "w")

        for j in range(0, len(all_indexes)):
            index_line = all_indexes[j]
            for i in range(0, len(index_line)):
                if i == 0:
                    f.write(str(index_line[i]) + ",")
                    if str(index_line[i]) == str(key):
                        print_end = False
                        f.write(str(loc) + ",")
                elif i != len(index_line) - 1:
                    f.write(str(index_line[i]) + ",")
                else:
                    f.write(str(index_line[i]))
            f.write("\n")

        if str(key) in self._data.keys():
            current_locations = self._data[key]
            current_locations.append(loc)
            self._data[key] = current_locations
        else:
            self._data[key] = [loc]

        if print_end:
            contents = str(key) + "," + str(loc)
            f.write(contents)

        f.close()

        f = open(self._location, 'r')
        final_lines = []
        for line in f:
            if not line.isspace():
                final_lines.append(line)
        f.close()

        with open(self._location, 'w') as f:
            f.writelines(final_lines)