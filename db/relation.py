from btree.Btree import *
from .errors import *
import os
import arff
from .index import Index, IndexSet
import copy


class Tuple:
    def __init__(self, primary_key, attributes, values, split_abutes=True):
        self._data = []
        self._primary_key = primary_key
        # self._attributes = {}
        # self._domains = {}
        #
        if split_abutes:
        #     i = 0
        #     for abute in attributes:
        #         self._attributes[abute['name']] = i
        #         self._domains[abute['name']] = abute['domain']
        #         i += 1
            for value in values:
                self._data.append(value['value'])
        else:
        #     self._attributes = attributes
            self._data = values

    def get_value_for_index(self, i):
        return self._data[i]

    def _get_data(self):
        return self._data

    def merge(self, new_tuple):
        abutes = {}
        # abutes = copy.deepcopy(self._attributes).update(new_tuple.get_attributes())
        new_data = self._data + new_tuple._get_data()
        return Tuple(self._primary_key, abutes, new_data, False)

    # def set_attributes(self, abutes):
    #     self._attributes = abutes

    # def get_attributes(self):
    #     return self._attributes

    def print(self):
        for d in self._data:
            if d is None:
                print("? ", end='')
            else:
                print(str(d) + " ", end='')

    # def value_for_attribute(self, attribute):
    #     if attribute not in self._attributes.keys():
    #         return None
    #     return self._data[self._attributes[attribute]]

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


# TODO: Probably relation needs to not organize data on the primary key due to combo primary keys
class Relation:
    def __init__(self, schema, relation_name, index_set, master_relation=False, data=None):
        # self._data = Btree(5)
        if data:
            self._data = data
        else:
            self._data = {}
        self._primary_key = schema['primary_key']
        self._attributes = schema['attributes']
        self._location = schema['location']
        self._name = relation_name
        self._index_set = index_set
        self._master_relation = master_relation
        self._attribute_row_counts = {}
        self._set_attribute_row_counts(self._attributes)

        if self._master_relation:
            self._load_file()

    def get_attribute_row_counts(self):
        return self._attribute_row_counts

    def set_data(self, data):
        self._data = data

    def update_right_join_attributes(self, right_rel, increment_right):
        new_attributes = right_rel.get_attributes_for_right_join(increment_right)
        attribute_counts = right_rel.get_attribute_row_counts()
        new_attribute_counts = {}
        for k, v in attribute_counts.items():
            new_attribute_counts['right_side_' + str(k)] = v + increment_right

        self._attributes = copy.deepcopy(self._attributes) + new_attributes
        self._attribute_row_counts = copy.deepcopy(self._attribute_row_counts)
        self._attribute_row_counts.update(new_attribute_counts)
        # self._attribute_row_counts += right_rel.get_attribute_row_counts()

        # keys = list(self._data.keys())
        # attributes = self._data[keys[0]].get_attributes()
        #
        # right_rel
        #
        # new_attributes = {}
        # for key, value in attributes.items():
        #     new_attributes["right_side_" + str(key)] = value + increment_right
        # data_to_gen = copy.deepcopy(self._data)
        # for key in data_to_gen.keys():
        #     data_to_gen[key].set_attributes(new_attributes)
        #     new_right_side_data.append(data_to_gen[key])
        #
        # return new_right_side_data
        # final_data = self._data.items()

    def get_attributes_for_right_join(self, increment_right):
        new_attributes = []
        new_attribute_names = copy.deepcopy(self._attributes)
        for abute in new_attribute_names:
            new_abute = {}
            new_abute['name'] = "right_side_" + str(abute['name'])
            new_abute['domain'] = abute['domain']
            new_attributes.append(new_abute)
            # new_attributes["right_side_" + str(key)] = value + increment_right
        return new_attributes

    def get_data_for_right_join(self):
        return [v for k,v in self._data.items()]

    def print(self):
        for key, value in self._data.items():
            value.print()
            print("\n")

    # def join(self, relation, attribute_left, attribute_right):
    #     schema = {'attributes': self._attributes, 'location': None, 'primary_key': self._primary_key}
    #     result = Relation(schema, "join_" + self._name + "_" + relation._name, self._index_set)
    #     if attribute_left == self._primary_key:
    #         new_data = {}
    #         joining_relation = None
    #         for key in self._data.keys():
    #             joining_relation = relation.select(attribute_right, key)
    #             right_data = joining_relation.get_data_for_right_join(len(self._attributes))
    #             i = 0
    #             for d in right_data:
    #                 new_data[str(key) + "_" + str(i)] = self._data[key].merge(d)
    #                 i += 1
    #         result.set_data(new_data)
    #         result.update_right_join_attributes(joining_relation, len(self._attributes))
    #         return result
    #     elif self._index_set.find_index(attribute_left):
    #         new_data = {}
    #         joining_relation = None
    #         for key, value in self._data.items():
    #             joining_key = self._value_for_attribute(value, attribute_left)
    #             joining_relation = relation.select(attribute_right, joining_key)
    #             right_data = joining_relation.get_data_for_right_join()
    #             i = 0
    #             for d in right_data:
    #                 new_data[str(key) + "_" + str(i)] = self._data[key].merge(d)
    #                 i += 1
    #         result.set_data(new_data)
    #         result.update_right_join_attributes(joining_relation, len(self._attributes))
    #         return result
        # elif self._index_set.find_index(attribute):
        #     select_index = self._index_set.find_index(attribute)
        #     hashes = select_index.find(value)
        #     new_data = {}
        #     for key in hashes:
        #         new_item = self._data[key]
        #         new_data[key] = new_item
        #     result.set_data(new_data)
        #     return result
        # else:
        #     new_data = {}
        #     for key, pair in self._data.items():
        #         if value == pair.value_for_attribute(attribute):
        #             new_data[key] = pair
        #     result.set_data(new_data)
        #     return result
    def join(self, relation, attribute_left, attribute_right):
        schema = {'attributes': self._attributes, 'location': None, 'primary_key': self._primary_key}
        result = Relation(schema, "join_" + self._name + "_" + relation._name, self._index_set)

        new_data = {}
        joining_relation = None

        join_type = "default"
        if attribute_left == self._primary_key:
            join_type = "primary_key"
        elif self._index_set.find_index(attribute_left):
            join_type = "index"

        for key, value in self._data.items():
            if join_type == "primary_key":
                joining_relation = relation.select(attribute_right, key)
            elif join_type == "index":
                joining_key = self._value_for_attribute(value, attribute_left)
                joining_relation = relation.select(attribute_right, joining_key)
            else:
                # TODO: joining when no index
                joining_relation = None

            right_data = joining_relation.get_data_for_right_join()
            i = 0
            for d in right_data:
                new_data[str(key) + "_" + str(i)] = self._data[key].merge(d)
                i += 1

        result.set_data(new_data)
        result.update_right_join_attributes(joining_relation, len(self._attributes))
        return result

    def select(self, attribute, value):
        schema = {'attributes': self._attributes, 'location': None, 'primary_key': self._primary_key}
        result = Relation(schema, "select_" + self._name, self._index_set)
        if attribute == self._primary_key:
            new_data = {}
            new_item = self._data[value]
            new_data[value] = new_item
            result.set_data(new_data)
            return result
        elif self._index_set.find_index(attribute):
            select_index = self._index_set.find_index(attribute)
            hashes = select_index.find(value)
            new_data = {}
            for key in hashes:
                new_item = self._data[key]
                new_data[key] = new_item
            result.set_data(new_data)
            return result
        else:
            new_data = {}
            for key, pair in self._data.items():
                if value == self._value_for_attribute(pair, attribute):
                    new_data[key] = pair
            result.set_data(new_data)
            return result

    def _value_for_attribute(self, tup, attribute):
        if attribute not in self._attribute_row_counts.keys():
            return None
        return tup.get_value_for_index(self._attribute_row_counts[attribute])

    def _load_file(self):
        if os.path.isfile(self._location + ".arff"):
            print("load file")
            primary_key = ""
            relation_data_file = arff.load(open(self._location + ".arff", 'r'))
            relation_data = relation_data_file['data']
            for tuple in relation_data:
                attributes = []
                for i in range(0, len(tuple)):
                    if self._attributes[i]['name'] == self._primary_key:
                        primary_key = tuple[i]
                    attributes.append({'attribute': self._attributes[i]['name'], 'value': tuple[i]})
                self._data[primary_key] = Tuple(primary_key, self._attributes, attributes)

    def _set_attribute_row_counts(self, attribute_counts):
        i = 0
        for abute in attribute_counts:
            self._attribute_row_counts[abute['name']] = i
            i += 1

    def _convert_arff_type(self, value_to_convert):
        if value_to_convert == "string":
            return "STRING"
        elif value_to_convert == "integer":
            return "NUMERIC"
        else:
            return "STRING"

    def _convert_new_attributes_to_array(self, attributes):
        new_attributes = {}
        for abute in attributes:
            new_attributes[abute['attribute']] = abute['value']

        new_attribute_array = []
        for abute in self._attributes:
            abute_name = abute['name']
            if abute_name in new_attributes.keys():
                new_attribute_array.append(new_attributes[abute_name])
            else:
                new_attribute_array.append(None)

        return new_attribute_array

    def _insert_to_file(self, attributes):
        arff_attributes = self._attributes

        arff_attributes = [(i['name'], self._convert_arff_type(i['domain'])) for i in arff_attributes]
        new_attributes_array = self._convert_new_attributes_to_array(attributes)

        relation_data = []

        if os.path.isfile(self._location + ".arff"):
            print("update file")
            relation_data_file = arff.load(open(self._location + ".arff", 'r'))
            relation_data = relation_data_file['data']

        relation_data.append(new_attributes_array)

        f = open(self._location + ".arff", "w")

        relation_new_table_data = {
            'relation': self._name,
            'attributes': arff_attributes,
            'data': relation_data
        }
        f.write(arff.dumps(relation_new_table_data))
        f.close()

    def insert_values(self, attributes):
        primary_key = ""

        for abute in attributes:
            if abute['attribute'] == self._primary_key:
                primary_key = abute['value']

        if primary_key == "":
            print("Emty primary key error / no primary key error")
            raise Error

        if primary_key in self._data.keys():
            print("Duplicate primary key error:")
            raise Error

        new_tuple = Tuple(primary_key, self._attributes, attributes)
        self._data[primary_key] = new_tuple

        # TODO: non-master relations may need to be able to add indexes
        if self._master_relation:
            for abute in attributes:
                attribute = abute['attribute']

                index = self._index_set.find_index(attribute)

                if index is not None:
                    value = abute['value']
                    index._add_index(value, primary_key)

            self._insert_to_file(attributes)
            print(self._data)
        # self._data.insert(new_tuple)
        # self._data.print_tree()


