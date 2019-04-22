from .metadata import Metadata
from .relation import Relation
from .index import Index, IndexSet
import os
from .errors import *

# TODO: Right now indexes, primary, and foreign keys can only be one attribute
# TODO: This is the highest priority feature to add
# TODO: Next priority is add def project - this will remove and allow renaming of attributes
# TODO: Update
# TODO: Delete
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
    # left_on is the left attribute to join on (so in the above it would be x)
    # right_on is the right one
    # update_indexes defaults to true - when set to true the join will updates the indexes for the new relation
    # it returns. Because this on (very) large rleations can take time, the option exists to join without updating
    # indexes. If this is done however, it is best not to perform any select operations on the resulting relation
    # since it will have no indexes
    #
    # Example (to join relation C with itself on the value attribute and update the indexes):
    # c = db.select("C")
    # db.join(c, c, "value", "value")
    #
    # TODO: Currently the join is only an equal-join
    def join(self, left_relation, right_relation, left_on, right_on, update_indexes=True):
        return left_relation.join(right_relation, left_on, right_on, update_indexes)

    # relation - this can either be a string or relation object. If it is a string it will find a saved relation
    # with the name provided. If it is a relation object it will perform the selection on that object
    # where: this is an array of where clauses in the form of:
    # [{"attribute1": 'attribute_name', "value1": 'value_of_attribute_selecting_on'},
    # {"attribute2": 'attribute_name', "value2": 'value_of_attribute_selecting_on'}]
    # if the where clause is empty select just returns the relation object for relation.
    #
    # Examples (produce the same result):
    # db.select("B", [{"attribute": 'value2', "value": '25'}])
    # db.select(db.select("B"), [{"attribute": 'value2', "value": '25'}])
    #
    # TODO: Currently the select is only select =. Needs more functionality
    def select(self, relation, where=None):
        if not isinstance(relation, Relation):
            if relation in self._relations.keys():
                relation = self._relations[relation]
            else:
                raise SQLInputError(str(relation) + " is not a relation in the database")
        if where is None or len(where) == 0:
            return relation

        condition = where.pop(0)
        selected_relation = relation.select(condition['attribute'], condition['value'])
        if len(where) == 0:
            return selected_relation
        else:
            return self.select(selected_relation, where)

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
    def create_indexes(self, relation, attributes, types, names):
        self._md.add_indexes(relation, names, types, attributes)

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






                # Random junk
# # f = open("./demofile3.arff", "w")
# #
# # relation_metadata = {
# #     'relation': 'relation_metadata',
# #     'attributes': [
# #         ('relation_name', 'STRING'),
# #         ('location', 'STRING'),
# #         ('primary_key', 'STRING')
# #     ],
# #     'data': [
# #         ["students", "./data/students", "student_id"],
# #         ["universities", "./data/universities", "university_id"],
# #     ]
# # }
# #
# # f.write(arff.dumps(relation_metadata))
# # f.close()
#
# arff_file = arff.load(open("./demofile3.arff", 'r'))
# abutes = arff_file['attributes']
# data = arff_file['data']
# # #
# f = open("./demofile3.arff", "w")
# f.write(arff.dumps(arff_file))
# # #
# # #
# # #
# # #
# f.close()
#
#
# # def load_arff_file(self, file_name):
# #     print("Loading arff file")
# #     print("Loading arff file", file=open("adult.out", "a"))
# #     arff_file = arff.load(open(file_name))
# #     abutes = arff_file['attributes']
# #
# #     data = arff_file['data']
# #
# #     numeric_keys = [x[0] for x in abutes if self._get_abute_numeric(x)]
# #     non_numeric_keys = [x[0] for x in abutes if not self._get_abute_numeric(x)]
# #
# #     # abutes = [x[0] for x in abutes]
# #     # columns_change = {i: x for i, x in enumerate(abutes)}
# #     #
# #     # df = df.rename(index=str, columns=columns_change)
# #     self._numeric_data = numeric_keys
# #     self._non_numeric_columns = non_numeric_keys
# #
# #
# # def _get_abute_numeric(self, ab):
# #     numeric = ab[1]
# #     if numeric == 'NUMERIC' or numeric == 'REAL' or numeric == 'INTEGER':
# #         return True
# #     else:
# #         return False