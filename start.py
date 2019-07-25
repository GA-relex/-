#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2019/7/18 16:17
# @Author  : relex
# @File    : start.py
import os
import pickle


def initialize(cls, file_name):
    if os.path.exists("db\\%s.pk" % file_name):
        with open("db\\%s.pk" % file_name, "rb") as f:
            cls.list = pickle.load(f)
    else:
        cls.list = []


def save(cls_list, file_name):
    with open("db\\%s.pk" % file_name, "wb") as f:
        pickle.dump(cls_list, f)


def print_list(obj_list):
    for n, val in enumerate(obj_list):
        print("%s、%s" % (n + 1, val[0]))


def find_obj(obj_list, find_str):
    for val in obj_list:
        if find_str == val[0]:
            return val[1]


def select_operation(main_list, classes=None):
    print_list(main_list)
    while True:
        identity_id = input("请选择序号：").strip()
        if identity_id.isdigit():
            if 0 < int(identity_id) <= len(main_list):
                if len(main_list[-1]) == 1:
                    if int(identity_id) == len(main_list):
                        save(School.list, "School_list")
                        save(Teacher.list, "Teacher_list")
                        save(Student.list, "Student_list")
                        exit("欢迎使用选课系统，再见！")
                    else:
                        getattr(classes, main_list[int(identity_id) - 1][1])()
                        break
                else:
                    return main_list[int(identity_id) - 1][1]
            else:
                print("输入有误，请重新输入")
        else:
            print("输入有误，请重新输入")


def input_digit(print_str):
    while True:
        price = input(print_str).strip()
        if price.isdigit():
            return price
        print("你的输入有误，请重新输入")


class School:
    def __init__(self, name):
        self.name = name
        self.course_list = []
        self.teacher_list = []

    @classmethod
    def initialize(cls):
        initialize(cls, "School_list")

    @classmethod
    def create_school(cls):
        name = input("请输入学校地址：").strip()
        obj = cls(name)
        cls.list.append([name, obj])
        print("%s校区创建成功！" % name)

    @classmethod
    def create_teacher(cls):
        name = input("请输入老师姓名：").strip()
        password = input("请输入老师密码：").strip()
        print("请选择任教校区\n现有校区：")
        new_teacher = Teacher(name, password)
        school = select_operation(cls.list)
        Teacher.list.append([name, new_teacher])
        school.teacher_list.append(Teacher.list[-1])
        print("%s校区：%s老师创建成功！" % (school.name, name))

    @classmethod
    def create_classes(cls):
        print("请选择要创建班级的校区\n现有校区：")
        school = select_operation(cls.list)
        print("请选择班级教授的课程：\n现有课程：")
        course = select_operation(school.course_list)
        name = input("请输入班级名称：").strip()
        name = name + ":" + course.name
        new_classes = Classes(name)
        course.classes_list.append([name, new_classes])
        print("请选择班级授课老师：\n现有老师：")
        teacher = select_operation(school.teacher_list)
        teacher.classes_list.append(course.classes_list[-1])
        print("%s校区：%s班创建成功！" % (school.name, name))

    @classmethod
    def creat_course(cls):
        name = input("请输入课程名称：").strip()
        period = input("请输入课程周期：").strip()
        price = input_digit("请输入课程价格：")
        obj = Course(name, period, price)
        print("请选择课程开设校区\n现有校区：")
        school = select_operation(cls.list)
        school.course_list.append([name, obj])
        print("%s校区：%s课程创建成功！" % (school.name, name))


class Student:
    pass_obj = None

    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.pay_course_name = []
        self.score = "暂无成绩"

    @classmethod
    def initialize(cls):
        initialize(cls, "Student_list")

    @classmethod
    def register(cls):
        name = input("请输入姓名：").strip()
        if find_obj(cls.list, name):
            print("学生已存在!")
        else:
            password = input("请输入密码：").strip()
            print("请选择注册校区：")
            school = select_operation(School.list)
            new_student = Student(name, password)
            new_student.school = school
            cls.list.append([name, new_student])
            cls.pass_obj = new_student
            print("注册成功！")

    @classmethod
    def payment(cls):
        Student.pass_obj = login(cls)
        student = Student.pass_obj
        if student:
            print("请选择你想学习的课程：")
            course = select_operation(student.school.course_list)
            if course.name in student.pay_course_name:
                print("课程已交过费用，请勿重复交费！")
            else:
                print("课程价格:%s元，请交费。" % course.price)
                student.pay_course_name.append(course.name)
                print("交费成功")

    @classmethod
    def select_classes(cls):
        Student.pass_obj = login(cls)
        student = Student.pass_obj
        if student:
            print("请选择班级：")
            classes = select_operation(student.school.classes_list)
            if classes.course.name in student.pay_course_name:
                if find_obj(classes.student_list, student.name):
                    print("你已经在%s班级中！")
                else:
                    classes.student_list.append([student.name, student])
                    print("班级选择成功！")
            else:
                print("课程%s还未交费。" % classes.course.name)


class Classes:
    def __init__(self, name):
        self.name = name
        self.student_list = []


class Course:
    def __init__(self, name, period, price):
        self.name = name
        self.period = period
        self.price = price
        self.classes_list = []

class Manage:
    @staticmethod
    def check(obj):
        print("%s老师，你现在的班级有：" % obj.name)
        print_list(obj.classes_list)
        print("end".center(20, "-"))

    @staticmethod
    def add(obj):
        Manage.check(obj)
        print("%s校区的班级有：" % obj.school.name)
        classes = select_operation(obj.school.classes_list)
        if [classes.name, classes] in obj.classes_list:
            print("班级已存在！")
        else:
            obj.classes_list.append([classes.name, classes])
            print("班级已添加！")

    @staticmethod
    def del_course(obj):
        print("请你选择要删除的班级：")
        classes = select_operation(obj.classes_list)
        obj.classes_list.remove([classes.name, classes])
        print("已成功删除班级%s" % classes.name)


class Teacher:
    pass_obj = None

    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.classes_list = []

    @classmethod
    def initialize(cls):
        initialize(cls, "Teacher_list")

    def manage_classes(self):
        manage_list = [
            ["查看班级", Manage.check],
            ["添加班级", Manage.add],
            ["删除班级", Manage.del_course]
        ]
        print("请选择操作序号：")
        select_operation(manage_list)(self)

    def select_classes(self):
        print("请选择你要上课的班级：")
        classes = select_operation(self.classes_list)
        print("选择成功，你将要在%s上课" % classes.name)

    def check_student(self):
        print("请选择班级：")
        classes = select_operation(self.classes_list)
        print("学员列表如下：")
        print_list(classes.student_list)

    def change_score(self):
        print("请选择学员所在班级：")
        classes = select_operation(self.classes_list)
        print("请选择要修改成绩的学员：")
        student = select_operation(classes.student_list)
        print("学员%s的成绩为：%s" % (student.name, student.score))
        chenge_score = input("请输入修改后的成绩：")
        student.score = chenge_score
        print("修改成功！")


class Account:
    @staticmethod
    def administrator():
        administrator_login_list = [
            ["创建学校", "create_school"],
            ["创建讲师", "create_teacher"],
            ["创建班级", "create_classes"],
            ["创建课程", "creat_course"],
            ["退出"]
        ]
        while True:
            select_operation(administrator_login_list, School)

    @staticmethod
    def student():
        student_login_list = [
            ["注册", "register"],
            ["交费", "payment"],
            ["选择班级", "select_classes"],
            ["退出"]
        ]
        while True:
            select_operation(student_login_list, Student)

    @staticmethod
    def teacher():
        teacher_login_list = [
            ["管理班级", "manage_classes"],
            ["选择上课班级", "select_classes"],
            ["查看班级学员列表", "check_student"],
            ["修改学员成绩", "change_score"],
            ["退出"]
        ]
        while True:
            Teacher.pass_obj = login(Teacher)
            select_operation(teacher_login_list, Teacher.pass_obj)


def login(cls):
    if cls.pass_obj:
        return cls.pass_obj
    else:
        name = input("请输入姓名：").strip()
        obj = find_obj(cls.list, name)
        if obj:
            password = input("请输入密码：").strip()
            if obj.password == password:
                return obj
            else:
                print("密码输入错误！")
        else:
            print("用户不存在")


def main():
    School.initialize()
    Teacher.initialize()
    Student.initialize()
    print("欢迎来到选课系统！")
    main_list = [
        ["学生", "student"],
        ["教师", "teacher"],
        ["管理员", "administrator"],
        ["退出"]
    ]
    select_operation(main_list, Account)


main()
