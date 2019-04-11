from collections import defaultdict
from prettytable import PrettyTable
import unittest

class University: #get students and instructors and grades in this class and try to print it
    def __init__(self,wdir,ptables = True):
        self.wdir = wdir
        self.students = dict()


class Student:
    pt_hdr = ['CWID','Name','Completed Courses']

    def __init__(self,cwid,name,major):
        self.cwid = cwid
        self.name = name
        self.major = major
        self.courses =dict()

    def add_course(self,course,grade):
        self.courses[coures] = grade

    def pt_row(self):
        return [self.cwid,self.name,self.major,self.courses]




def student_test(self):

    expected = {'all key':['all values']}

    calculate = {cwid: student.pt_row() for cwid,studnet in self.repo.studnetsitem()}

    self.assertEqual(expected,calculate)



# CWID as a key and list as a value

#get a tuple to get all instructors's information
