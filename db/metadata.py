import os
import arff
from db.errors import *


class Metadata:
    def __init__(self):
        self._relation_metadata_fp = "./metadata/relation_metadata.arff"
        self._attribute_metadata_fp = "./metadata/attribute_metadata.arff"
        self._index_metadata_fp = "./metadata/index_metadata.arff"
        self._foreign_key_metadata_fp = "./metadata/foreign_key_metadata.arff"
        self._relation_md = []
        self._attribute_md = []
        self._index_md = []
        self._foreign_key_md = []

        self._relations = {}

        self._load_md_into_memory()
        self._save_metadata()

    def get_relations(self):
        self._build_relations_info()
        return self._relations

    def get_indexes(self):
        maped_indexes = set(map(lambda x: x[0], self._index_md))
        grouped_indexes = [[y for y in self._index_md if y[0] == x] for x in maped_indexes]
        meta_data_indexes = []
        for indice in grouped_indexes:
            if len(indice) > 1:
                index_name = indice[0][0]
                index_relation = indice[0][1]
                index_type = "type"
                index_attribute = ""
                for i in range(0, len(indice)):
                    indx_abute = indice[i]
                    indx_abute = indx_abute[3]
                    index_attribute += indx_abute
                    if i != len(indice) - 1:
                        index_attribute += "+"
                meta_data_indexes.append([index_name, index_relation, index_type, index_attribute])
            else:
                meta_data_indexes.append(indice[0])
        return meta_data_indexes

    def _build_relations_info(self):
        for rel in self._relation_md:
            relation = rel[0]

            attributes = []
            for abute in self._attribute_md:
                if abute[0] == relation:
                    attributes.append({"name": abute[1], "domain": abute[2]})

            self._relations[relation] = {'attributes': attributes, 'location': rel[1], 'primary_key': rel[2]}

    def _load_md_into_memory(self):
        if os.path.isfile(self._relation_metadata_fp):
            relation_md_f = arff.load(open(self._relation_metadata_fp, 'r'))
            self._relation_md = relation_md_f['data']
        else:
            self._relation_md = []

        if os.path.isfile(self._attribute_metadata_fp):
            attribute_md_f = arff.load(open(self._attribute_metadata_fp, 'r'))
            self._attribute_md = attribute_md_f['data']
        else:
            self._attribute_md = []

        if os.path.isfile(self._index_metadata_fp):
            index_md_f = arff.load(open(self._index_metadata_fp, 'r'))
            self._index_md = index_md_f['data']
        else:
            self._index_md = []

        if os.path.isfile(self._foreign_key_metadata_fp):
            foreign_key_md_f = arff.load(open(self._foreign_key_metadata_fp, 'r'))
            self._foreign_key_md = foreign_key_md_f['data']
        else:
            self._foreign_key_md = []

    def _save_relation_metadata(self):
        if len(self._relation_md) > 0:
            f = open(self._relation_metadata_fp, "w")
            relation_metadata = {
                'relation': 'relation_metadata',
                'attributes': [
                    ('relation_name', 'STRING'),
                    ('location', 'STRING'),
                    ('primary_key', 'STRING')
                ],
                'data': self._relation_md
            }
            f.write(arff.dumps(relation_metadata))
            f.close()
        elif os.path.isfile(self._relation_metadata_fp):
            os.remove(self._relation_metadata_fp)

    def _save_attribute_metadata(self):
        if len(self._attribute_md) > 0:
            f = open(self._attribute_metadata_fp, "w")
            attribute_metadata = {
                'relation': 'attribute_metadata',
                'attributes': [
                    ('relation_name', 'STRING'),
                    ('attribute_name', 'STRING'),
                    ('domain_type', 'STRING'),
                ],
                'data': self._attribute_md
            }
            f.write(arff.dumps(attribute_metadata))
            f.close()
        elif os.path.isfile(self._attribute_metadata_fp):
            os.remove(self._attribute_metadata_fp)

    def _save_index_metadata(self):
        if len(self._index_md) > 0:
            f = open(self._index_metadata_fp, "w")
            index_metadata = {
                'relation': 'index_metadata',
                'attributes': [
                    ('index_name', 'STRING'),
                    ('relation_name', 'STRING'),
                    ('index_type', 'STRING'),
                    ('index_attributes', 'STRING')
                ],
                'data': self._index_md
            }
            f.write(arff.dumps(index_metadata))
            f.close()
        elif os.path.isfile(self._index_metadata_fp):
            os.remove(self._index_metadata_fp)

    def _save_foreign_key_meadata(self):
        if len(self._foreign_key_md) > 0:
            f = open(self._foreign_key_metadata_fp, "w")
            foreign_key_metadata = {
                'relation': 'foreign_key_metadata',
                'attributes': [
                    ('relation', 'STRING'),
                    ('attribute', 'STRING'),
                    ('foreign_key', 'STRING'),
                    ('foreign_key_table', 'STRING'),
                ],
                'data': self._foreign_key_md
            }
            f.write(arff.dumps(foreign_key_metadata))
            f.close()
        elif os.path.isfile(self._foreign_key_metadata_fp):
            os.remove(self._foreign_key_metadata_fp)

    def _save_metadata(self):
        self._save_relation_metadata()
        self._save_attribute_metadata()
        self._save_index_metadata()
        self._save_foreign_key_meadata()

    def add_relation(self, relation_name, primary_key, primary_key_domain_type):
        existing_relations = [rel for rel in self._relation_md if rel[0] == relation_name]

        if len(existing_relations) > 0:
            raise DuplicateRelation

        self._relation_md.append([relation_name, "./data/" + relation_name, primary_key])
        self._save_relation_metadata()
        self.add_attributes(relation_name, [primary_key], [primary_key_domain_type])
        self.add_indexes(relation_name, ["index_" + relation_name + "_" + primary_key + "_primary_key"], [["type"]],
                         [[primary_key]])

    def add_attributes(self, relation_name, attribute_names, domain_types):
        for i in range(len(attribute_names)):
            self._add_attribute(relation_name, attribute_names[i], domain_types[i])
        self._save_attribute_metadata()

    def add_indexes(self, relation_name, index_names, index_type_arrays, index_attribute_arrays):
        for i in range(len(index_names)):
            self._check_for_duplicate_index(index_names[i])

        for i in range(len(index_names)):
            self._add_index(index_names[i], relation_name, index_type_arrays[i], index_attribute_arrays[i])
        self._save_index_metadata()

    def add_foreign_keys(self, relation, attributes, foreign_keys, foreign_key_tables):
        for i in range(len(attributes)):
            self._check_for_duplicate_fk(relation, attributes[i])

        for i in range(len(attributes)):
            self._add_foreign_key(relation, attributes[i], foreign_keys[i], foreign_key_tables[i])
        self._save_foreign_key_meadata()

    def delete_fk(self, relation, attribute):
        self._foreign_key_md = [fk for fk in self._foreign_key_md if fk[0] != relation and fk[1] != attribute]
        self._save_foreign_key_meadata()

    def delete_index(self, index_name):
        self._index_md = [ix for ix in self._index_md if ix[0] != index_name]
        self._save_index_metadata()

    def delete_relation(self, relation):
        self.delete_attributes(relation, None)
        self._relation_md = [rel for rel in self._relation_md if rel[0] != relation]
        self._save_relation_metadata()

    def delete_attributes(self, relation, attribute):
        indexes = [ix for ix in self._index_md if
                        ((relation is not None and ix[1] == relation and ix[3] == attribute) or
                                      (attribute is None and ix[1] == relation))]

        foreign_keys = [fk for fk in self._foreign_key_md if
                        ((relation is not None and fk[0] == relation and fk[1] == attribute) or
                                      (attribute is None and fk[0] == relation) or
                         (relation is not None and fk[3] == relation and fk[2] == attribute) or
                                      (attribute is None and fk[3] == relation))]

        if len(foreign_keys) > 0:
            raise ForeignKeyError

        if len(indexes) > 0:
            raise IndexesError

        self._attribute_md = [abute for abute in self._attribute_md
                              if not ((attribute is not None and abute[0] == relation and abute[1] == attribute) or
                                      (attribute is None and abute[0] == relation))]
        self._save_attribute_metadata()

    def _add_attribute(self, relation_name, attribute_name, domain_type):
        existing_attributes = [abutes for abutes in self._attribute_md if
                               abutes[0] == relation_name and abutes[1] == attribute_name]

        if len(existing_attributes) > 0:
            raise DuplicateAttribute

        self._attribute_md.append([relation_name, attribute_name, domain_type])

    def _check_for_duplicate_index(self, index_name):
        existing_indexes = [indexes for indexes in self._index_md if
                            indexes[0] == index_name]
        # existing_indexes = [indexes for indexes in self._index_md if
        #                 indexes[0] == index_name or (indexes[1] == relation_name and
        #                                              indexes[3] == index_attributes)]

        if len(existing_indexes) > 0:
            raise DuplicateIndex

    def _add_index(self, index_name, relation_name, index_types, index_attributes):
        if len(index_types) != len(index_attributes):
            raise SQLInputError("New indexes must have an equal number of types and attributes")
        for i in range(len(index_attributes)):
            self._index_md.append([index_name, relation_name, index_types[i], index_attributes[i]])

    def _check_for_duplicate_fk(self, relation, attribute):
        existing_fks = [fk for fk in self._foreign_key_md if
                        fk[0] == relation and fk[1] == attribute]

        if len(existing_fks) > 0:
            raise DuplicateFK

    def _add_foreign_key(self, relation, attribute, foreign_key, foreign_key_table):
        self._foreign_key_md.append([relation, attribute, foreign_key, foreign_key_table])


# # Impossible foreign keys
# # Table already exists
# metadata.add_indexes("students", ["student_id_primary_key"], ["type"], ["student_id"])
# metadata.delete_fk("students", "university")
# metadata.delete_index("student_index")
# metadata.add_relation("students", "student_id", "STRING")

# metadata.delete_relation("students")
# metadata.add_foreign_key("students", "name", "no_key")
# print(metadata)

# # f = open("./metadata/attribute_metadata.arff", "w")
# #
#
#
# #
# # f.write(arff.dumps(relation_metadata))
# # f.close()
# #
# arff_file = arff.load(open("./metadata/attribute_metadata.arff", 'r'))
# abutes = arff_file['attributes']
# data = arff_file['data']
# print(data)
# # # #
# # f = open("./demofile3.arff", "w")
# # f.write(arff.dumps(attribute_metadata))
# # #
# # #
# # #
# # #
# # f.close()

