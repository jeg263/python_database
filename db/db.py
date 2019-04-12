from .metadata import Metadata
from .relation import Relation
import os


class DB:
    def __init__(self):
        self._md = Metadata()
        self._schemas = self._md.get_relations()
        self._relations = {}

        self._load_data()

    def _load_data(self):
        for relation in self._schemas.keys():
            # location = self._schemas[relation]['location']
            self._relations[relation] = Relation(self._schemas[relation])
            # if os.path.isfile(location):
            #     print("load file")
            # else:
            #     self._relations[relation] = Relation(self._schemas[relation])

    # Values should be an array of the format: [{attribute: 'atribute_name', value: 'value'}]
    def insert_tuple(self, relation, values):
        rel = self._relations[relation]
        if rel is not None:
            rel.insert_values(values)

        print("Insert table")

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