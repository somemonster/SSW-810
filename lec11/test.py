import os
import sqlite3
from prettytable import PrettyTable
from collections import defaultdict

DB_FILE = "/Users/123/python/lec11/lec11.db"
db = sqlite3.connect(DB_FILE)

pt = PrettyTable(field_names=['CWID','Name','Dept','Course','students'])
for row in db.execute("SELECT Instructors.CWID,Instructors.Name,Instructors.Dept,A.Course,A.students from Instructors join(select Instructor_CWID,Course,count(*)as students from Grades group by Course)A on Instructors.CWID = A.Instructor_CWID order by Name"):
    pt.add_row(row)
print(pt)