from .metadata import Metadata
from .relation import Relation
from .index import Index, IndexSet
import os
from .errors import *


class DB:
    def __init__(self):
        self._md = Metadata()
        self._schemas = self._md.get_relations()
        self._relations = {}

        self._load_indexes()
        self._load_data()
        self._load_fks()

    def _refresh(self):
        self._md = Metadata()
        self._schemas = self._md.get_relations()
        self._relations = {}

        self._load_indexes()
        self._load_data()
        self._load_fks()

    def drop_foreign_key(self, relation, attribute):
        self._md.delete_fk(relation, attribute)

    def drop_index(self, name):
        self._md.delete_index(name)
        if os.path.isfile("./index/" + name + ".csv"):
            os.remove("./index/" + name + ".csv")

    def drop_table(self, relation):
        if relation not in self._relations.keys():
            raise SQLInputError("Relation does not exist")
        self._md.delete_relation(relation)
        relation = self._relations.pop(relation)
        relation.drop(self)

    # relation is a relation object
    # tuples is an array of attribute arrays, so takes the form:
    # [[{attribute: 'atribute_name', value: 'value'}], [{attribute: 'atribute_name', value: 'value'}]]
    # See the insert tuple method to see example of that method
    def insert_tuples(self, relation, tuples):
        for tup in tuples:
            self.insert_tuple(relation, tup)
        self._refresh()
        return relation

    # left_relation - relation object, left relation when saying:
    # FROM relation_left, relation_right WHERE relation_left.x = relation_right.y
    # right_relation - relation object is the right one
    # left_on is an array of the left attribute to join on (so in the above it would be x)
    # right_on is an array of the right ones
    # update_indexes defaults to true - when set to true the join will updates the indexes for the new relation
    # it returns. Because this on (very) large rleations can take time, the option exists to join without updating
    # indexes. If this is done however, it is best not to perform any select operations on the resulting relation
    # since it will have no indexes
    #
    # operation is the type of join, so =, >, <, !=, >=, <=
    #
    # Example (to join relation C with itself on the value attribute and update the indexes):
    # c = db.select("C")
    # db.join(c, c, ["value"], ["value"], "operation")
    def join(self, left_relation, right_relation, left_on, right_on, operations=["="], update_indexes=True):
        if len(left_on) != len(right_on):
            raise SQLInputError("The number of join conditions on the left and right sides must equal one another")
        return left_relation.join(self, right_relation, left_on, right_on, update_indexes, operations)

    # relation - this can either be a string or relation object. If it is a string it will find a saved relation
    # with the name provided. If it is a relation object it will perform the selection on that object
    # where: this is an array of where clauses in the form of:
    # [{"attribute1": 'attribute_name', "value1": 'value_of_attribute_selecting_on', "operation": "="},
    # {"attribute2": 'attribute_name', "value2": 'value_of_attribute_selecting_on', "operation": ">"}]
    # if the where clause is empty select just returns the relation object for relation.
    #
    # Examples (produce the same result):
    # db.select("B", [{"attribute": 'value2', "value": '25', "operation": "="}])
    # db.select(db.select("B"), [{"attribute": 'value2', "value": '25', "operation": ">"}])
    def select(self, relation, where=None):
        if not isinstance(relation, Relation):
            if relation in self._relations.keys():
                relation = self._relations[relation]
            else:
                raise SQLInputError(str(relation) + " is not a relation in the database")
        if where is None or len(where) == 0:
            return relation

        for abute in where:
            if abute['attribute'].find("right_side_") != -1 and abute['attribute'] not in relation._attribute_row_counts.keys():
                abute['attribute'] = abute['attribute'][len("right_side_"):]

        combo_select_attributes = relation.check_for_combo_select(where)
        where = combo_select_attributes + where

        for combo_select_abute in combo_select_attributes:
            attribute = combo_select_abute['attribute']
            attributes_to_delete = set(attribute.split("+"))

            where = [x for x in where if x['attribute'] not in attributes_to_delete]

        condition = where.pop(0)
        operation = "="
        if "operation" in condition.keys():
            operation = condition["operation"]
        selected_relation = relation.select(condition['attribute'], condition['value'], operation)
        if len(where) == 0:
            return selected_relation
        else:
            return self.select(selected_relation, where)

    def project(self, relation, attributes, as_attributes=None, deepcopy=False, lose_rhs= False):
        return relation.project(attributes, as_attributes, deepcopy, lose_rhs=lose_rhs)

    def update(self, relation, values, where):
        relations_to_update = self.select(relation, where)

        for rel in self._fks.keys():
            if relation.get_name() == rel:
                attributes_with_fks = self._fks[rel]
                for attribute in attributes_with_fks.keys():
                    if attribute in set([x['attribute'] for x in values]):
                        resulting_attributes = self.project(relations_to_update, [attribute], deepcopy=True)
                        fk_values = resulting_attributes.get_attribute_value_array()
                        fk_values = [x[0]['value'] for x in fk_values]

                        fk_arrays = attributes_with_fks[attribute]
                        for fk_relationship in fk_arrays:
                            relation_to = fk_relationship[0]
                            attribute_to = fk_relationship[1]
                            for value in fk_values:
                                fks_to_break_on = self.select(relation_to, [{"attribute": attribute_to, "value": value}])
                                if len(fks_to_break_on) > 0:
                                    raise SQLInputError("Foreign key constraint")

        tuples_to_update = len(relations_to_update)
        if tuples_to_update == 0:
            raise SQLInputError("No tuples to update with those parameters")

        for value in values:
            domain_of_abute = relation._domains[value['attribute']]
            if domain_of_abute == 'integer':
                value['value'] = str(int(value['value']))
            elif domain_of_abute == "float":
                value['value'] = str(float(value['value']))

            if value['attribute'] == relation._primary_key:
                if tuples_to_update > 1:
                    raise SQLInputError("Cannot update the primary key of more than one tuple to the same value")
                if value['value'] in relation.get_primary_keys():
                    raise SQLInputError("An attribute already exists with the primary key you are updating")

        relations_to_update = relations_to_update.update_all(values)
        values_to_insert = relations_to_update.get_attribute_value_array()

        self.delete(relation, where, override_fk_constraints=True)
        for value in values_to_insert:
            self.insert_tuple(relation, value)
        return relation

    def delete(self, relation, where, override_fk_constraints=False):
        relation_to_remove = self.select(relation, where)
        if not override_fk_constraints:
            for rel in self._fks.keys():
                if relation.get_name() == rel:
                    attributes_with_fks = self._fks[rel]
                    for attribute in attributes_with_fks.keys():
                        resulting_attributes = self.project(relation_to_remove, [attribute], deepcopy=True)
                        fk_values = resulting_attributes.get_attribute_value_array()
                        fk_values = [x[0]['value'] for x in fk_values]

                        fk_arrays = attributes_with_fks[attribute]
                        for fk_relationship in fk_arrays:
                            relation_to = fk_relationship[0]
                            attribute_to = fk_relationship[1]
                            for value in fk_values:
                                fks_to_break_on = self.select(relation_to, [{"attribute": attribute_to, "value": value}])
                                if len(fks_to_break_on) > 0:
                                    raise SQLInputError("Foreign key constraint")

        return relation.delete(relation_to_remove)

    # relation is a relation object
    # Values should be an array of the format: [{attribute: 'atribute_name', value: 'value'}]
    # db.insert_tuple(db.select("B"),
    #                 [{"attribute": "id", "value": 115}, {"attribute": "value", "value": 1},
    #                  {"attribute": "value2", 13: str(j)}, {"attribute": "value3", "value": 15}])
    def insert_tuple(self, relation, values):
        simple_fks = self._md.get_simple_fks()
        for fk in simple_fks:
            loc_relation = fk[3]
            attribute = fk[2]
            relation_abute = fk[1]
            for v in values:
                if v['attribute'] == relation_abute:
                    resulting_fks = self.select(loc_relation, [{'attribute': attribute, "value": v['value'], "operation": "="}])
                    if len(resulting_fks) == 0:
                        raise SQLInputError("Cannot insert foreign keys until those keys are created")

                # attributes_with_fks = self._fks[rel]
                # for attribute in attributes_with_fks.keys():
                #     resulting_attributes = self.project(relation_to_remove, [attribute], deepcopy=True)
                #     fk_values = resulting_attributes.get_attribute_value_array()
                #     fk_values = [x[0]['value'] for x in fk_values]
                #
                #     fk_arrays = attributes_with_fks[attribute]
                #     for fk_relationship in fk_arrays:
                #         relation_to = fk_relationship[0]
                #         attribute_to = fk_relationship[1]
                #         for value in fk_values:
                #             fks_to_break_on = self.select(relation_to, [{"attribute": attribute_to, "value": value}])
                #             if len(fks_to_break_on) > 0:
                #                 raise SQLInputError("Foreign key constraint")
        return relation.insert_values(values)

    # relation is a string with the name of the relation
    # each other variable is an array of what it is named, e.g.:
    # db.create_indexes("A", ["value"], ["type"], ["A_value_index"])
    def create_indexes(self, relation, attribute_arrays, type_arrays, names):
        self._md.add_indexes(relation, names, type_arrays, attribute_arrays)
        print("Index(es) created")
        self._refresh()

    # Pretty self explanatory - look at the example
    # db.create_table("B", "id", "string", ["value", "value2", "value3"],
    #                 ["string", "string", "string"])
    def create_table(self, relation, primary_keys, primary_key_domain, other_attributes, other_domains):
        primary_key = ""
        if len(primary_keys) == 1:
            primary_key = primary_keys[0]
            primary_key_domain = primary_key_domain[0]
        else:
            i = 0
            for abute in primary_keys:
                i += 1
                primary_key += abute
                if i != len(primary_keys):
                    primary_key += "+"
            other_attributes += primary_keys
            other_domains += primary_key_domain

        self._md.add_relation(relation, primary_key, primary_key_domain)
        self._md.add_attributes(relation, other_attributes, other_domains)
        if primary_key.find("+") != -1:
            type_array = []
            for i in range(0, len(primary_keys)):
                type_array.append("type")
            self.create_indexes(relation, [primary_keys], [type_array],
                                ["index_" + relation + "_" + primary_key + "_primary_key"])

        self._refresh()

    # FK
    # db.create_fks("A", ["value"], ["B"], ["id"])
    def create_fks(self, relation, attributes, foreign_keys, foreign_key_tables):
        # TODO: handle new fks when data already exists
        self._md.add_foreign_keys(relation, attributes, foreign_keys, foreign_key_tables)

    def _load_fks(self):
        self._fks = self._md.get_fks()

    # This will load all the indexes in the files into memory -
    # it determines what indexes need to be loaded based on the metadata
    def _load_indexes(self):
        index_md = self._md.get_indexes()
        indexes = {}
        for idx in index_md:
            index = Index(idx[0], idx[1], idx[3], master_index=True)

            # TODO: Eventually this should be changed to accept multiple indexes for the same attribute - use an array
            # at each index and then put combo indexes in an array for each combo they fit with
            if index.relation in indexes.keys():
                indexes[index.relation].add_index(index)
            else:
                indexes[index.relation] = IndexSet(index)

        self._indexes = indexes

    # This will load all of the initial relations into memory - it locates them from the metadata
    def _load_data(self):
        for relation in self._schemas.keys():
            self._relations[relation] = Relation(self._schemas[relation], relation, self._indexes[relation], True)


class DBParser(DB):
    def __init__(self):
        DB.__init__(self)

    def insert(self, relation, attributes, values):
        if len(attributes) != len(values):
            raise SQLInputError("The number of values must equal the number of attributes provided")

        insert_array = []
        for i in range(0, len(attributes)):
            insert_array.append({"attribute": attributes[i], "value": values[i]})

        relation = relation[0]

        result = self.insert_tuples(self.select(relation), [insert_array])
        print("Tuple(s) inserted into relation")
        return result

