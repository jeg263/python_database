from btree.Btree import *
from .errors import *
import os
import arff
from .index import Index, IndexSet
import copy
from .tuple import Tuple
from tabulate import tabulate
import operator


class Relation:
    def __init__(self, schema, relation_name, index_set, master_relation=False, data=None):
        if data:
            self._data = data
        else:
            self._data = {}
        self._primary_key = schema['primary_key']
        self._attributes = schema['attributes']
        self._domains = {}
        for abute in self._attributes:
            self._domains[abute['name']] = abute['domain']
        self._location = schema['location']
        self._name = relation_name
        self._index_set = index_set
        self._master_relation = master_relation
        self._attribute_row_counts = {}
        self._set_attribute_row_counts(self._attributes)

        if self._master_relation:
            self._load_file()

    def remove_duplicates(self):
        attribute_row_count_array = []
        for k, v in self._attribute_row_counts.items():
            attribute_row_count_array.append(v)

        duplicate_keys = []
        duplicates = set()
        for k, v in self._data.items():
            val_to_check = str(v.tabulation_values(attribute_row_count_array))
            if val_to_check in duplicates:
                duplicate_keys.append(k)
            else:
                duplicates.add(val_to_check)

        for key in duplicate_keys:
            self._data.pop(key)
        return self

    def get_name(self):
        return self._name

    def get_attribute_row_counts(self):
        return self._attribute_row_counts

    def get_index_set(self):
        return self._index_set

    def set_indexes(self, index_set):
        self._index_set = index_set

    def set_data(self, data):
        self._data = data

    def update_right_join_attributes(self, right_rel, increment_right, lhs_attribute_dict):
        new_attributes = right_rel.get_attributes_for_right_join(increment_right, lhs_attribute_dict)
        attribute_counts = right_rel.get_attribute_row_counts()
        new_attribute_counts = {}
        new_abute_dict = set()

        for abute in new_attributes:
            new_abute_dict.add(abute['name'])

        for k, v in attribute_counts.items():
            if 'right_side_' + str(k) in new_abute_dict:
                new_attribute_counts['right_side_' + str(k)] = v + increment_right
            else:
                new_attribute_counts[str(k)] = v + increment_right

        self._attributes = copy.deepcopy(self._attributes) + new_attributes
        self._domains = {}
        for abute in self._attributes:
            self._domains[abute['name']] = abute['domain']
        self._attribute_row_counts = copy.deepcopy(self._attribute_row_counts)
        self._attribute_row_counts.update(new_attribute_counts)

    def get_attributes_for_right_join(self, increment_right, lhs_attribute_dict):
        new_attributes = []
        new_attribute_names = copy.deepcopy(self._attributes)
        for abute in new_attribute_names:
            new_abute = {}
            if abute['name'] in lhs_attribute_dict.keys():
                new_abute['name'] = "right_side_" + str(abute['name'])
            else:
                new_abute['name'] = str(abute['name'])
            new_abute['domain'] = abute['domain']
            new_attributes.append(new_abute)
            # new_attributes["right_side_" + str(key)] = value + increment_right
        return new_attributes

    def get_primary_keys(self):
        return self._data.keys()

    def get_tuples(self):
        return self.get_data_for_right_join()

    def get_data_for_right_join(self):
        return [v for k,v in self._data.items()]

    def print(self):
        sorted_row_counts = sorted(self._attribute_row_counts.items(), key=operator.itemgetter(1))
        headers = [x[0] for x in sorted_row_counts]
        # headers = [x['name'] for x in self._attributes]

        attribute_row_count_array = []
        for k, v in self._attribute_row_counts.items():
            attribute_row_count_array.append(v)

        tabulation_values = []
        i = 0
        for key, value in self._data.items():
            if i < 300:
                tabulation_values.append(value.tabulation_values(attribute_row_count_array))
            else:
                break
            i += 1
        print(tabulate(tabulation_values, headers=headers))
        count_of_items = len(self._data.keys())
        if count_of_items > 300:
            print(". . . . . . ")
            print("Showing 300 of " + str(count_of_items) + " tupes in relation")

    def _remove_attributes(self, attributes):
        abute_set = set(attributes)
        self._attributes = [x for x in self._attributes if x['name'] not in abute_set]
        self._domains = {}
        for abute in self._attributes:
            self._domains[abute['name']] = abute['domain']

        deleted_indexes = {}

        for abute in attributes:
            deleted_indexes[abute] = self._attribute_row_counts.pop(abute, None)
        for abute in deleted_indexes.keys():
            for k, v in self._attribute_row_counts.items():
                if self._attribute_row_counts[k] > deleted_indexes[abute]:
                    self._attribute_row_counts[k] -= 1

        column_counts = []
        for k, v in deleted_indexes.items():
            column_counts.append(v)
        column_counts = sorted(column_counts, reverse=True)
        for k, v in self._data.items():
            v.delete_column_counts(column_counts, in_order=True)
            self._data[k] = v

    def join(self, db, relation, attributes_left, attributes_right, update_index_set=True, operation="="):
        schema = {'attributes': copy.deepcopy(self._attributes), 'location': None, 'primary_key': "fake_pk"}
        result = Relation(schema, "join_" + self._name + "_" + relation.get_name(), None)

        new_data = {}
        joining_relation = None

        rhs_join_index = Index("in_memory", "join_" + self._name + "_" + relation.get_name(), "join_to_id")
        lhs_join_index = Index("in_memory", "join_" + self._name + "_" + relation.get_name(), "join_to_id")

        # TODO: verify that this no joining on primary key works
        for key, value in self._data.items():
            joining_keys = self._values_for_attributes(value, attributes_left)
            attributes_right_to_join_on = []
            for i in range(0, len(attributes_right)):
                attributes_right_to_join_on.append(
                    {"attribute": attributes_right[i], "value": joining_keys[i], "operation": operation})
            joining_relation = db.select(relation, attributes_right_to_join_on)

            right_data = joining_relation.get_data_for_right_join()
            i = 0
            for d in right_data:
                if update_index_set:
                    lhs_join_index.add_index(key, str(key) + "_" + str(i))
                    rhs_join_index.add_index(d.get_primary_key(), str(key) + "_" + str(i))
                new_data[str(key) + "_" + str(i)] = self._data[key].merge(d)
                i += 1

        lhs_attribute_dict = {}
        for abute in self._attributes:
            lhs_attribute_dict[abute['name']] = 1

        if update_index_set:
            lhs_join_index_set = copy.deepcopy(self.get_index_set())
            lhs_join_index_set.add_sub_index(lhs_join_index)
            rhs_join_index_set = copy.deepcopy(relation.get_index_set())
            rhs_join_index_set.add_sub_index(rhs_join_index)

            for abute in rhs_join_index_set.get_index_attributes():
                i_to_add = rhs_join_index_set.find_index(abute)
                if abute in lhs_attribute_dict.keys():
                    i_to_add.update_attribute_name("right_side_" + abute)
                lhs_join_index_set.add_index(i_to_add)

            result.set_indexes(lhs_join_index_set)
        result.set_data(new_data)
        result.update_right_join_attributes(joining_relation, len(self._attributes), lhs_attribute_dict)

        attributes_to_remove = ["right_side_" + str(x) for x in attributes_right]
        all_attributes_in_result = set(result.get_attribute_row_counts().keys())

        new_attributes = list(all_attributes_in_result.difference(set(attributes_to_remove)))

        result = db.project(result, new_attributes)

        # result._remove_attributes(["right_side_" + str(x) for x in attributes_right])

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

    def __len__(self):
        return len(self._data)

    def constrain_attributes(self, attributes, as_attributes):
        self._attributes = [x for x in self._attributes if x['name'] in set(attributes)]
        new_attribute_counts = {}
        for i in range(0, len(attributes)):
            if attributes[i] in self._attribute_row_counts.keys():
                new_attribute_counts[as_attributes[i]] = self._attribute_row_counts[attributes[i]]

        self._attribute_row_counts = new_attribute_counts

        final_attributes = []
        for abute in self._attributes:
            abute_name = abute['name']
            for i in range(0, len(attributes)):
                if abute_name == attributes[i]:
                    abute['name'] = as_attributes[i]
                    final_attributes.append(abute)

        self._attributes = final_attributes
        self._domains = {}
        for abute in self._attributes:
            self._domains[abute['name']] = abute['domain']
        return self

    def project_indexes(self, attributes, as_attributes):
        return self._index_set.project_indexes(attributes, as_attributes)

    def project(self, attributes, as_attributes=None, deepcopy=False):
        if as_attributes is None:
            as_attributes = attributes

        if len(attributes) != len(as_attributes):
            raise SQLInputError("If changing the name of an attribute, every attribute name must be changed")

        # projected_attributes = [x for x in self._attributes if x['name'] in set(attributes)]

        if deepcopy:
            indexes_to_change = copy.deepcopy(self._index_set)
        else:
            indexes_to_change = self._index_set

        schema = {'attributes': self._attributes, 'location': None, 'primary_key': self._primary_key}
        projected_relation = Relation(schema, self._name, indexes_to_change, data=self._data)

        projected_relation = projected_relation.constrain_attributes(attributes, as_attributes)
        projected_relation.set_indexes(projected_relation.project_indexes(attributes, as_attributes))

        projected_relation = projected_relation.remove_duplicates()

        return projected_relation

    def delete(self, relation):
        tuples_to_delete = relation.get_tuples()
        primary_keys_to_delete = [x.get_primary_key() for x in tuples_to_delete]

        for key in primary_keys_to_delete:
            self._data.pop(key)

        if self._master_relation:
            self._remove_from_file(primary_keys_to_delete)

        return self

    def _remove_from_file(self, pks):
        arff_attributes = self._attributes

        arff_attributes = [(i['name'], self._convert_arff_type(i['domain'])) for i in arff_attributes]
        # new_attributes_array = self._convert_new_attributes_to_array(attributes)

        relation_data = []

        if os.path.isfile(self._location + ".arff"):
            print("update file")
            relation_data_file = arff.load(open(self._location + ".arff", 'r'))
            relation_data = relation_data_file['data']

        for index_of_primary_key in range(0, len(arff_attributes)):
            if arff_attributes[index_of_primary_key][0] == self._primary_key:
                break

        pks = set(pks)

        for i in range(0, len(relation_data)):
            if i >= len(relation_data):
                break
            pk = relation_data[i][index_of_primary_key]
            if pk in pks:
                relation_data.pop(i)
                i -= 1
        # print(relation_data)
        # relation_data.append(new_attributes_array)

        f = open(self._location + ".arff", "w")

        relation_new_table_data = {
            'relation': self._name,
            'attributes': arff_attributes,
            'data': relation_data
        }
        f.write(arff.dumps(relation_new_table_data))
        f.close()

    def _select_compare(self, lhs, rhs, operation, domain):
        if domain == "integer":
            lhs = int(lhs)
            rhs = int(rhs)
        elif domain == "float":
            lhs = float(lhs)
            rhs = float(rhs)

        if operation == "=":
            if lhs == rhs:
                return True
        elif operation == "!=":
            if lhs != rhs:
                return True
        elif operation == ">=" or operation == "=>":
            if lhs >= rhs:
                return True
        elif operation == "<=" or operation == "=<":
            if lhs <= rhs:
                return True
        elif operation == ">" or operation == ">":
            if lhs > rhs:
                return True
        else:
            if lhs < rhs:
                return True

        return False

    def select(self, attribute, value, operation="="):
        schema = {'attributes': copy.deepcopy(self._attributes), 'location': None, 'primary_key': self._primary_key}
        result = Relation(schema, "select_" + self._name, self._index_set)
        new_data = {}

        if self._index_set and self._index_set.find_index(attribute):
            select_index = self._index_set.find_index(attribute)
            domain = self._domains[attribute]
            hashes = select_index.find(value, domain=domain, operation=operation)
            for key in hashes:
                if key in self._data.keys():
                    new_item = self._data[key]
                    new_data[key] = new_item
        else:
            for key, pair in self._data.items():
                # if value == self._value_for_attribute(pair, attribute):
                if self._select_compare(self._value_for_attribute(pair, attribute), value,
                                        operation, self._domains[attribute]):
                    new_data[key] = pair

        result.set_data(new_data)
        result = result.remove_duplicates()
        return result

    def _values_for_attributes(self, tup, attributes):
        values = []
        for abute in attributes:
            value = self._value_for_attribute(tup, abute)
            if value is None:
                raise SQLInputError("Nonexistent attribute passed to query")
            values.append(value)
        return values

    def _value_for_attribute(self, tup, attribute):
        if attribute not in self._attribute_row_counts.keys():
            return None
        return tup.get_value_for_index(self._attribute_row_counts[attribute])

    def _load_file(self):
        if os.path.isfile(self._location + ".arff"):
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
        return "STRING"
        # if value_to_convert == "string":
        #     return "STRING"
        # elif value_to_convert == "integer":
        #     return "NUMERIC"
        # else:
        #     return "STRING"

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

    def get_attribute_value_array(self):
        attribute_value_array = []
        for k, v in self._data.items():
            attribute_list = []
            for attribute, index in self._attribute_row_counts.items():
                attribute_list.append({"attribute": attribute, "value": v.get_value_for_index(index)})
            attribute_value_array.append(attribute_list)
        return attribute_value_array

    def update_all(self, values):
        if len(values) <= 0:
            return self
        else:
            value_to_update = values.pop(0)
            for k, v in self._data.items():
                v.update_value_for_index(self._attribute_row_counts[value_to_update['attribute']], value_to_update['value'])

            return self.update_all(values)

    def insert_values(self, attributes):
        primary_key = ""

        for abute in attributes:
            domain_of_abute = self._domains[abute['attribute']]
            if domain_of_abute == 'integer':
                abute['value'] = str(int(abute['value']))
            elif domain_of_abute == "float":
                abute['value'] = str(float(abute['value']))

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
                    index.add_index(value, primary_key)

            combo_attributes = self.check_for_combo_select(attributes)
            for combo_abute in combo_attributes:
                index = self._index_set.find_index(combo_abute['attribute'])
                index.add_index(combo_abute['value'], primary_key)

            self._insert_to_file(attributes)

    def check_for_combo_select(self, attributes):
        attributes_to_search_combos_on = [x['attribute'] for x in attributes]
        attributes_to_search_combos_on = sorted(attributes_to_search_combos_on)
        combination_indexes = self._index_set.find_combination_indexes(attributes_to_search_combos_on)

        attribute_values = {}
        for abute in attributes:
            attribute_values[abute['attribute']] = abute['value']

        attribute_names_and_values = []

        for combo_abute in combination_indexes:
            combote_abute_name = ""
            combo_abute_value = ""

            i = 1
            for abute in combo_abute:
                combote_abute_name += abute
                combo_abute_value += str(attribute_values[abute])
                if i != len(combo_abute):
                    combote_abute_name += "+"
                    combo_abute_value += "+"
                i += 1

            new_combo_attribute = {}
            new_combo_attribute['attribute'] = combote_abute_name
            new_combo_attribute['value'] = combo_abute_value
            attribute_names_and_values.append(new_combo_attribute)

        return attribute_names_and_values

        # self._data.insert(new_tuple)
        # self._data.print_tree()


