from btree.Btree import *
from .errors import *
import os
import arff
from .index import Index, IndexSet
import copy
from .tuple import Tuple


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

    def get_index_set(self):
        return self._index_set

    def set_indexes(self, index_set):
        self._index_set = index_set

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

    def join(self, relation, attribute_left, attribute_right, update_index_set=True):
        # TODO: Join should lose an attribute
        # self._primary_key - updating is different
        schema = {'attributes': self._attributes, 'location': None, 'primary_key': "fake_pk"}
        result = Relation(schema, "join_" + self._name + "_" + relation._name, None)

        new_data = {}
        joining_relation = None

        rhs_join_index = Index("in_memory", "join_" + self._name + "_" + relation._name, "join_to_id")
        lhs_join_index = Index("in_memory", "join_" + self._name + "_" + relation._name, "join_to_id")

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
                if update_index_set:
                    lhs_join_index.add_index(key, str(key) + "_" + str(i))
                    rhs_join_index.add_index(d.get_primary_key(), str(key) + "_" + str(i))
                new_data[str(key) + "_" + str(i)] = self._data[key].merge(d)
                i += 1

        if update_index_set:
            lhs_join_index_set = copy.deepcopy(self.get_index_set())
            lhs_join_index_set.add_sub_index(lhs_join_index)
            rhs_join_index_set = copy.deepcopy(relation.get_index_set())
            rhs_join_index_set.add_sub_index(rhs_join_index)

            for abute in rhs_join_index_set.get_index_attributes():
                i_to_add = rhs_join_index_set.find_index(abute)
                i_to_add.update_attribute_name("right_side_" + abute)
                lhs_join_index_set.add_index(i_to_add)

            result.set_indexes(lhs_join_index_set)
        result.set_data(new_data)
        result.update_right_join_attributes(joining_relation, len(self._attributes))

        # if update_index_set:
        #     # TODO: What happens if no indexes
        #     left_index_abutes = list(self._index_set.get_index_attributes())
        #     right_index_abutes = list(relation.get_index_set().get_index_attributes())
        #
        #     right_index_abutes = ["right_side_" + str(abute) for abute in right_index_abutes]
        #     left_index_abutes += right_index_abutes
        #
        #     result.build_index_set_with_attributes(left_index_abutes)

        return result

    def _add_sub_index(self, sub_index):
        self._index_set.add_sub_index(sub_index)

    def build_index_set_with_attributes(self, attributes):
        indexes = []
        if len(attributes) > 0:
            for abute in attributes:
                new_index = Index("memory_index", self._name, abute)
                for k, v in self._data.items():
                    key = self._value_for_attribute(v, abute)
                    new_index.add_index(key, k)
                indexes.append(new_index)
            new_index_set = IndexSet(indexes.pop(0))
            for indx in indexes:
                new_index_set.add_index(indx)
            self._index_set = new_index_set

    def select(self, attribute, value):
        # TODO ensure all values are distinct
        schema = {'attributes': self._attributes, 'location': None, 'primary_key': self._primary_key}
        result = Relation(schema, "select_" + self._name, self._index_set)
        new_data = {}

        if attribute == self._primary_key:
            new_item = self._data[value]
            new_data[value] = new_item
        elif self._index_set and self._index_set.find_index(attribute):
            select_index = self._index_set.find_index(attribute)
            hashes = select_index.find(value)
            for key in hashes:
                if key in self._data.keys():
                    new_item = self._data[key]
                    new_data[key] = new_item
        else:
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


