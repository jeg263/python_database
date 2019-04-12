from db.db import DB

db = DB()
db.insert_tuple("students", [{"attribute": "student_id", "value": "30"}])
db.insert_tuple("students", [{"attribute": "student_id", "value": "45"}])

db.insert_tuple("students", [{"attribute": "student_id", "value": "10"}])
# db.create_table("students", "student_id", "string", ["full_name", "phone_number", "age", "university"],
#                 ["string", "string", "integer", "string"])
#
# db.create_table("universities", "university_id", "string", ["city"],
#                 ["string"])
# db.create_fks("students", ["university"], ["university_id"], ["universities"])