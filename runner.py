from db.db import DB
from db.errors import *

# Need pip install tabulate

try:
    db = DB()
    # db.create_table("Course", "id", "string", ["professor", "year", "student_id"],
    #                 ["string", "string", "string"])
    # db.create_indexes("Course", [["professor", "year"]], [["type", "type"]], ["course_professor_year_index"])

    db.select("B").print()
    # db.update(db.select("C"), [{'attribute': "value", "value": "2"}], [{"attribute": "id", "value": "1"}]).print()
    # db.insert_tuple(db.select("Course"), [{"attribute": "id", "value": "beg263"}, {"attribute": "professor", "value": "Woods"},
    #                     {"attribute": "year", "value": "2016"}, {"attribute": "student_id", "value": "id"}])

    # db.insert_tuple(db.select("C"),
    #                 [{"attribute": "id", "value": 500}, {"attribute": "value", "value": "2"}])

    c = db.select("C", [{'attribute': "id", "value": "10", "operation": "<="}])
    c.print()
    # db.update(c, [{'attribute': "id", "value": "101"}], [{"attribute": "id", "value": "2"}]).print()
    j = db.join(c, db.select("B"), ["id"], ["id"], ">")
    j.print()
    db.project(j, ["value"], ["value2"]).print()

    # courses = db.select("Course", [{"attribute": "professor", "value": "Woods"},
    #                     {"attribute": "year", "value": "2016"}, {"attribute": "id", "value": "beg263"}]).print()


    # # db.select("Q")
    # db.select("B", [{"attribute": 'value2', "value": '25'}])
    # print("break")
    # db.select(db.select("B"), [{"attribute": 'value2', "value": '25'}])
    # c = db.select("C")
    # j = db.join(c, c, "value", "value")
    #
    # db.select(j, [{"attribute": 'id', "value": '5'}]).print()
except SQLInputError as err:
    print("SQL Input Error: " + str(err.args[0]))
# for i in range(1, 1001):
#     db.insert_tuple("D",
#                     [{"attribute": "id", "value": str(i)}, {"attribute": "value", "value": str(1)}])
#     db.select("B", [{"attribute": 'value2', "value": '25'}])

# j = 0
# for i in range(1, 5001):
#     if j > 250:
#         j = 0
#     db.insert_tuple("B",
#                     [{"attribute": "id", "value": str(i)}, {"attribute": "value", "value": str(i)},
#                      {"attribute": "value2", "value": str(j)}, {"attribute": "value3", "value": str(j)}])
#     j += 1

    # db.select("A", [{"attribute": 'id', "value": '1'}])

# db.create_table("A", "id", "string", ["value"],
#                 ["string"])
# db.create_table("B", "id", "string", ["value", "value2", "value3"],
#                 ["string", "string", "string"])
# db.create_table("C", "id", "string", ["value"],
#                 ["string"])
# db.create_table("D", "id", "string", ["value"],
#                 ["string"])
#
# db.create_indexes("A", ["value"], ["type"], ["A_value_index"])
# db.create_indexes("B", ["value"], ["type"], ["B_value_index"])
# db.create_indexes("B", ["value2"], ["type"], ["B_value2_index"])
# db.create_indexes("C", ["value"], ["type"], ["C_value_index"])
# db.create_indexes("D", ["value"], ["type"], ["D_value_index"])
#
# db.create_fks("A", ["value"], ["B"], ["id"])


# TODO: Foreign key insert and delete errors
# db.create_fks("A", ["value"], ["B"], ["id"])


# db.select("students", [{"attribute": 'phone_number', "value": '24'}])
# db.insert_tuple("students", [{"attribute": "student_id", "value": "24"}, {"attribute": "university", "value": "24"}])

# db.insert_tuple("students", [{"attribute": "student_id", "value": "45"}])
#
# db.insert_tuple("students", [{"attribute": "student_id", "value": "10"}])






# db.create_indexes("students", ["university"], ["type"], ["student_university_index"])

# db.create_table("students", "student_id", "string", ["full_name", "phone_number", "age", "university"],
#                 ["string", "string", "integer", "string"])
#
# db.create_table("universities", "university_id", "string", ["city"],
#                 ["string"])
# db.create_fks("students", ["university"], ["university_id"], ["universities"])