# reference from:https://github.com/timshine
import os
import unittest
import sqlite3
from prettytable import PrettyTable
from collections import defaultdict

DB_FILE = "/Users/123/python/lec11/lec11.db"
db = sqlite3.connect(DB_FILE)

pt = PrettyTable(field_names=['CWID','Name','Dept','Course','students'])
for row in db.execute("SELECT Instructors.CWID,Instructors.Name,Instructors.Dept,A.Course,A.students from Instructors join(select Instructor_CWID,Course,count(*)as students from Grades group by Course)A on Instructors.CWID = A.Instructor_CWID order by Name"):
    pt.add_row(row)
print(pt)



def file_reader(path,number_files,split_type = '\t'):
    try:
        fp = open(path,'r')
    except FileNotFoundError:
        raise FileNotFoundError("Can't find a file,please try again")
    else:
        with fp:
            for n,line in enumerate(fp):
                fields = line.strip('\n').split(split_type)
                if len(fields) != number_files:
                    raise ValueError("Error with the format of fields,please input the right format")
                else:
                    yield fields



class Repository:

    def __init__(self,directory,prettytable = False):
        self.students = dict()
        self.instructors = dict()
        self.majors = dict()
        try:
            os.chdir(directory)
        except FileNotFoundError:
            raise FileNotFoundError("Can't get the directory,please try again")
        else:
            students_path = os.path.join(directory,"students.txt")
            instructors_path =os.path.join(directory,"instructors.txt")
            majors_path = os.path.join(directory,"majors.txt")
            grades_path = os.path.join(directory,"grades.txt")
            self.open_students_file(students_path,'\t')
            self.open_instructors_file(instructors_path,'\t')
            self.open_grades_file(grades_path,'\t')
            self.open_majors_file(majors_path,'\t')
        
        if prettytable == True:
            print("Major Summary")
            self.print_majors()
            print("\nStudent Summary")
            self.print_students()
            print("\nInstructors Summary")
            self.print_instructors()

    def open_majors_file(self,path,split_type):
        number_files = 3
        for major,tflag,tcourse in file_reader(path,number_files,'\t'):
            if major not in self.majors:
                self.majors[major] = Major(major)
            self.majors[major].add_course(tflag,tcourse)
            
    
    def open_students_file(self,path,split_type):
        number_files = 3
        for CWID,Name,Major in file_reader(path,number_files,'\t'):
            self.students[CWID] = Student(CWID,Name,Major)
            if Major in self.students:
                self.students[CWID].judge_coures(self.majors[Major])
                

    def open_instructors_file(self,path,split_type):
        number_files =3
        for CWID,Name,Dept in file_reader(path,number_files,'\t'):
            self.instructors[CWID] = Instructor(CWID,Name,Dept)

    def open_grades_file(self,path,split_type):
        number_files =4
        for CWID,Course,Grade,T_CWID in file_reader(path,number_files,'\t'):
            if CWID in self.students:
                self.students[CWID].add_course(Course,Grade)
            else:
                raise ValueError("There is a CWID with no students")
            if T_CWID in self.instructors:
                self.instructors[T_CWID].add_course(Course)
            else:
                raise ValueError("There is a T_CWID with no instructors")
    
    
    def print_majors(self):
        pt = PrettyTable(field_names=['Dept','Required','Electives'])
        for major in self.majors:
            pt.add_row(self.majors[major].Majors_info())
        print(pt)

    
    
    def print_students(self):
        pt = PrettyTable(field_names=['CWID','Name','Major','Completed Courses','Remaining Required','Remaining Electives'])
        for CWID in self.students:
            pt.add_row(self.students[CWID].Students_info())
        print(pt)

    def print_instructors(self):
        pt = PrettyTable(field_names=['CWID','Name','Dept','Course','Students'])
        for CWID in self.instructors:
            for Course in self.instructors[CWID].Instructors_info():
                pt.add_row(Course)
        print(pt)



class Major:
    def __init__(self,Dept):
        self.Dept=Dept
        self.Required = set()
        self.Electives = set()

    def add_course(self,tflag,tcourse):
        if tflag == 'R':
            self.Required.add(tcourse)
        if tflag == 'E':
            self.Electives.add(tcourse)

    def Majors_info(self):
        return [self.Dept,sorted(self.Required),sorted(self.Electives)]


class Student:
    def __init__(self,CWID,Name,Major):
        self.CWID = CWID
        self.Name = Name
        self.Major= Major
        self.taken_coureses = defaultdict(str)
        self.Completed_courses = set()
        self.Remaining_required = set()
        self.Remaining_electives = set()

    def add_course(self,Course,Grade):
        self.taken_coureses[Course] = Grade
        if Grade in ['A+','A','A-','B+','B','B-','C+','C']:
            self.Completed_courses.add(Course)
            self.Remaining_required = self.Remaining_required.difference(self.Completed_courses)
            if len(self.Remaining_electives.intersection(self.Completed_courses))>0:
                self.Remaining_electives = {'None'}

    def judge_coures(self,Major):
        self.Remaining_required = Major.Required
        self.Remaining_electives = Major.Electives


    def Students_info(self):
        return [self.CWID,self.Name,self.Major,sorted(self.Completed_courses),sorted(self.Remaining_required),sorted(self.Remaining_electives)]
        
class Instructor:
    def __init__(self,CWID,Name,Dept):
        self.CWID = CWID
        self.Name = Name
        self.Dept = Dept
        self.Course = defaultdict(int)


    def add_course(self,Course):
        self.Course[Course] +=1

    def Instructors_info(self):
        for Course,Students in self.Course.items():
            yield [self.CWID,self.Name,self.Dept,Course,Students]

def main():
    directory = r'/Users/123/python/lec11'
    lec9 = Repository(directory,prettytable=True)
    
class RepositoryTest(unittest.TestCase):
    def right_input(self):
        directory = r'/Users/123/python/lec11'
        test_file = os.path.join(directory,'right_input')
        student_test = {10183:Student('10183','Chapman, O','SFEN')}
        instructor_test = {98760 :Instructor('98760','Darwin, C','SYEN')}
        self.assertTrue(student_test.keys()==Repository(test_file).students.keys())
        self.assertTrue(instructor_test.keys()==Repository(test_file).instructors.keys())


if __name__ == '__main__':
    main()

if __name__ == '__main__':
    unittest.main(exit=False,verbosity=2)