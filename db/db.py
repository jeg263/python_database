from .metadata import Metadata
from .relation import Relation
from .index import Index, IndexSet
import os
from .errors import *

# TODO: Keys with multiple attributes, including primary key


class DB:
    def __init__(self):
        self._md = Metadata()
        self._schemas = self._md.get_relations()
        self._relations = {}

        self._load_indexes()
        self._load_data()

    def _load_indexes(self):
        index_md = self._md.get_indexes()
        indexes = {}
        for idx in index_md:
            index = Index(idx[0], idx[1], idx[3])

            # TODO: Eventually this should be changed to accept multiple indexes for the same attribute - use an array
            # at each index and then put combo indexes in an array for each combo they fit with
            if index.relation in indexes.keys():
                indexes[index.relation].add_index(index)
            else:
                indexes[index.relation] = IndexSet(index)

        self._indexes = indexes

    def _load_data(self):
        for relation in self._schemas.keys():
            # location = self._schemas[relation]['location']
            self._relations[relation] = Relation(self._schemas[relation], relation, self._indexes[relation], True)
            # if os.path.isfile(location):
            #     print("load file")
            # else:
            #     self._relations[relation] = Relation(self._schemas[relation])

    def insert_tuples(self, relation, tuples):
        for tup in tuples:
            self.insert_tuple(relation, tup)

    def join(self, left_relation, right_relation, left_on, right_on):
        return left_relation.join(right_relation, left_on, right_on)
        # if relation in self._relations.keys() and with_relation in self._relations.keys():
        #     left_rel = self._relations[relation]
        #     right_rel = self._relations[with_relation]
        #     join_rel = left_rel.join(right_rel, left_on, right_on)
        #     join_rel.print()

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

    # Values should be an array of the format: [{attribute: 'atribute_name', value: 'value'}]
    def insert_tuple(self, relation, values):
        rel = self._relations[relation]
        if rel is not None:
            rel.insert_values(values)

        print("Insert table")

    def create_indexes(self, relation, attributes, types, names):
        # TODO: The database needs to index all the data if an index is new but data already exists
        self._md.add_indexes(relation, names, types, attributes)

    def create_table(self, relation, primary_key, primary_key_domain, other_attributes, other_domains):
        self._md.add_relation(relation, primary_key, primary_key_domain)
        self._md.add_attributes(relation, other_attributes, other_domains)

    def create_fks(self, relation, attributes, foreign_keys, foreign_key_tables):
        self._md.add_foreign_keys(relation, attributes, foreign_keys, foreign_key_tables)


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