from .metadata import Metadata
from .relation import Relation
from .index import Index, IndexSet
import os
from .errors import *

# TODO: Delete - fix referential integrity + handle deleting indexes
# TODO: Update - fix referential integrity

# TODO: Drop table
# TODO: Drop index
# TODO: Drop attributes

# TODO: Aggregation functions

# TODO: Multiple attribute primary keys and foreign keys (hardest)
# TODO: Project - projecting primary keys, when it removes duplicates

# TODO: add index after data has been placed in relation
# TODO: Build test cases
# TODO: Documentation
# TODO: verify that input supplied is actually the type said
# TODO: Simple optimization
#       Ordering join statements


class DB:
    def __init__(self):
        self._md = Metadata()
        self._schemas = self._md.get_relations()
        self._relations = {}

        self._load_indexes()
        self._load_data()

    # relation is a relation object
    # tuples is an array of attribute arrays, so takes the form:
    # [[{attribute: 'atribute_name', value: 'value'}], [{attribute: 'atribute_name', value: 'value'}]]
    # See the insert tuple method to see example of that method
    def insert_tuples(self, relation, tuples):
        for tup in tuples:
            self.insert_tuple(relation, tup)

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
    def join(self, left_relation, right_relation, left_on, right_on, operation="=", update_indexes=True):
        if len(left_on) != len(right_on):
            raise SQLInputError("The number of join conditions on the left and right sides must equal one another")
        return left_relation.join(self, right_relation, left_on, right_on, update_indexes, operation)

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

    def project(self, relation, attributes, as_attributes=None, deepcopy=False):
        return relation.project(attributes, as_attributes, deepcopy)

    # TODO: test to make sure you don't update a foreign key someone depends upon
    # The other main thing I have to do though is check for referential integrity before and after
    # I also need to verify that none of the new values will cause problems before I delete
    def update(self, relation, values, where):
        # TODO: if you update a primary key a lot of indexes need to change
        # TODO: if you update a primary key it needs to not just change the tuples as currently
        # TODO: need to have an override constrains variable for delete
        relations_to_update = self.select(relation, where)
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

        self.delete(relation, where)
        for value in values_to_insert:
            self.insert_tuple(relation, value)
        return relation

    # TODO: Needs to update the file
    # TODO: referential integrity
    def delete(self, relation, where):
        # TODO: if you delete a tuple some indexes likely change

        relation_to_remove = self.select(relation, where)
        return relation.delete(relation_to_remove)

    # relation is a relation object
    # Values should be an array of the format: [{attribute: 'atribute_name', value: 'value'}]
    # db.insert_tuple(db.select("B"),
    #                 [{"attribute": "id", "value": 115}, {"attribute": "value", "value": 1},
    #                  {"attribute": "value2", 13: str(j)}, {"attribute": "value3", "value": 15}])
    def insert_tuple(self, relation, values):
        relation.insert_values(values)

    # relation is a string with the name of the relation
    # each other variable is an array of what it is named, e.g.:
    # db.create_indexes("A", ["value"], ["type"], ["A_value_index"])
    # TODO: The database needs to index all the data if an index is new but data already exists
    # TODO: Also will need to add index to indexes array
    def create_indexes(self, relation, attribute_arrays, type_arrays, names):
        self._md.add_indexes(relation, names, type_arrays, attribute_arrays)

    # Pretty self explanatory - look at the example
    # db.create_table("B", "id", "string", ["value", "value2", "value3"],
    #                 ["string", "string", "string"])
    def create_table(self, relation, primary_key, primary_key_domain, other_attributes, other_domains):
        self._md.add_relation(relation, primary_key, primary_key_domain)
        self._md.add_attributes(relation, other_attributes, other_domains)

    # FK
    # db.create_fks("A", ["value"], ["B"], ["id"])
    def create_fks(self, relation, attributes, foreign_keys, foreign_key_tables):
        # TODO: handle new fks when data already exists
        self._md.add_foreign_keys(relation, attributes, foreign_keys, foreign_key_tables)

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