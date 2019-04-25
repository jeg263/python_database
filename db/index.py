from .errors import *
import os
import arff
import sys
import fileinput


class IndexSet:
    def __init__(self, start_index):
        self._data = {}
        self._combination_indexes = {}
        self.relation = start_index.relation
        self.add_index(start_index)

    def add_sub_index(self, sub_index):
        for k,v in self._data.items():
            v.add_sub_index(sub_index)

    def add_index(self, index):
        if index.attribute not in self._data.keys():
            self._data[index.attribute] = index
            if index.combination_index == True:
                self._add_combination_index(index)

    def _add_combination_index(self, index):
        abutes = index.attribute.split("+")
        self._add_combination_attributes(abutes, self._combination_indexes)

    def _add_combination_attributes(self, abutes, combination_dictionary):
        new_dictionary = {}
        if len(abutes) == 0:
            return {}
        else:
            indexing_abute = abutes.pop(0)
            if indexing_abute not in combination_dictionary.keys():
                combination_dictionary[indexing_abute] = self._add_combination_attributes(abutes, new_dictionary)
                return combination_dictionary
            else:
                self._add_combination_attributes(abutes, combination_dictionary[indexing_abute])
                return combination_dictionary

    def get_index_attributes(self):
        return self._data.keys()

    def _flatten_combination_array(self, lhs, rhs):
        combination_array = []
        if len(rhs) == 0:
            combination_array.append([lhs])
            return combination_array

        for obj in rhs:
            combination_array.append([lhs] + obj)
        return combination_array

    def _find_combination_index_recursive(self, rge, attributes, combination_dict):
        if len(combination_dict.keys()) == 0:
            return []

        result = []

        for j in rge:
            if attributes[j] in combination_dict.keys():
                combination_array = self._flatten_combination_array(attributes[j],
                                                                    self._find_combination_index_recursive(range(j + 1,
                                                        len(attributes)), attributes, combination_dict[attributes[j]]))
                result += combination_array
        return result

    def find_combination_indexes(self, attributes):
        combination_attributes = []
        for i in range(0, len(attributes) - 1):
            if attributes[i] in self._combination_indexes.keys():
                combination_attributes += self._flatten_combination_array(attributes[i],
                                        self._find_combination_index_recursive(range(i + 1, len(attributes)),
                                                        attributes, self._combination_indexes[attributes[i]]))

        return combination_attributes

    def project_indexes(self, attributes, as_attributes):
        attributes_to_delete = []
        new_items = {}
        for k, v in self._data.items():
            i = 0
            for abute in attributes:
                if abute == k and k != as_attributes[i]:
                    new_items[as_attributes[i]] = v
                    v.attribute = as_attributes[i]
                    attributes_to_delete.append(k)
                i += 1
        for abute in attributes_to_delete:
            self._data.pop(abute)

        for k, v in new_items.items():
            self._data[k] = v

        return self

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

        self.combination_index = False
        has_multiple_abutes = self.attribute.find("+")
        if has_multiple_abutes != -1:
            self.combination_index = True

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

    def find(self, key, domain="string", operation="="):
        index_data = []

        # if domain == "string" and operation == "=":
        #     if key in self._data.keys():
        #         index_data = self._data[key]
        d = {}
        if domain == "string":
            d = self._data
        elif domain == "integer":
            d = {int(k): v for k, v in self._data.items()}
            key = int(key)
        elif domain == "float":
            d = {float(k): v for k, v in self._data.items()}
            key = float(key)

        if operation == "=":
            if key in d.keys():
                index_data = d[key]
        else:
            if operation == "!=":
                keys = list(set(d.keys()).difference(set([key])))
            elif operation == ">=" or operation == "=>":
                keys = [k for k in d.keys() if k >= key]
            elif operation == "<=" or operation == "=<":
                keys = [k for k in d.keys() if k <= key]
            elif operation == ">" or operation == ">":
                keys = [k for k in d.keys() if k > key]
            else:
                keys = [k for k in d.keys() if k < key]
            for key_to_i in keys:
                index_data += d[key_to_i]
        key = str(key)

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