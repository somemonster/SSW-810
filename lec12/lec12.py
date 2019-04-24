import sqlite3
from flask import Flask, render_template

DB_FILE = '/Users/123/python/lec12/lec11.db'

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello world! This is Flask!"

@app.route('/Goodbye')
def see_ya():
    return "See you later!"

@app.route('/instructor_table')
def instructor_table():
    query =""" SELECT Instructors.CWID,Instructors.Name,Instructors.Dept,A.Course,A.students from Instructors join(select Instructor_CWID,Course,count(*)as students from Grades group by Course)A on Instructors.CWID = A.Instructor_CWID order by Name"""
    db = sqlite3.connect(DB_FILE)
    results = db.execute(query)

    data =[{'cwid':cwid,'name':name,'dept':dept,'course':course,'cnt':cnt}
    for cwid,name,dept,course,cnt in results]

    db.close()

    return render_template('parameters.html',
    title='Stevens Repository',
    table_title='Instructor table',
    Instructors = data)
app.run(debug=True)