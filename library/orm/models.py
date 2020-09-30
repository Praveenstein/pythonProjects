# -*- coding: utf-8 -*-
""" Main class module for storing library information

This script contains all the class details required to perform the
orm_queries based SQL operations, it contains the following classes

    * Department
    * Students
    * Professors
    * Authors
    * Books
    * BooksAuthor
    * Staffs
    * BookItem
    * StudentActivity
    * ProfessorActivity
    * StudentBorrow
    * ProfessorBorrow

This script requires that the following packages be installed within the Python
environment you are running this script in.

    * sqlalchemy - Package used to connect to a database and do SQL operations using orm_queries

"""

# Standard Imports
from datetime import date, timedelta
import enum

# External Imports
from sqlalchemy import Column, Integer, Enum, \
    String, Float, DATE, Boolean, ForeignKey, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import TIMESTAMP
from sqlalchemy import text
from sqlalchemy.schema import FetchedValue

__author__ = 'praveen@gyandata.com'

Base = declarative_base()


class BookStatus(enum.Enum):
    """ Enum class to store the status of book items"""
    AVAILABLE = "AVAILABLE"
    UNAVAILABLE = "UNAVAILABLE"
    LOST = "LOST"


class Department(Base):
    """This class stores the information pertaining to the Department Table of the Database.

    Attributes
    ----------
    dept_id : int
        Primary Key of Department table.

    name : str
        Name of department.

    students : list
        List of students belonging to this department.

    staffs : list
        List of professors belonging to this department.


    books : json
        List of books belonging to this department.

    """

    __tablename__ = 'department'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    dept_id = Column(Integer(), primary_key=True)
    name = Column(String(255), index=True, nullable=False)

    created_on = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP"))
    last_updated = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        server_onupdate=FetchedValue())

    students = relationship("Students", backref=backref('department'), order_by="Students.reg_id",
                            cascade="all, delete, delete-orphan")
    staffs = relationship("Professors", backref=backref('department'),
                          order_by="Professors.employee_code",
                          cascade="all, delete, delete-orphan")
    books = relationship("Books", backref=backref('department'), order_by="Books.isbn_id",
                         cascade="all, delete, delete-orphan")


class Students(Base):
    """This class stores the information pertaining to the Students.

    Attributes
    ----------
    reg_id : int
        Primary Key of Students table.

    name : str
        Name of student.

    doj : DATE
        Date of joining of student

    dept_id : int
        Foreign key referring to Department Table, denoting the department
        to which the student belongs to

    activities : list
        List of activities belonging to this student.

    """
    __tablename__ = 'students'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    reg_id = Column(Integer(), primary_key=True)
    name = Column(String(255), index=True, nullable=False)
    doj = Column(DATE(), nullable=False)
    dept_id = Column(Integer(), ForeignKey('department.dept_id'), nullable=False)

    created_on = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP"))
    last_updated = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        server_onupdate=FetchedValue())

    activities = relationship("StudentActivity", backref=backref('student'),
                              order_by="StudentActivity.trans_id",
                              cascade="all, delete, delete-orphan")


class Professors(Base):
    """This class stores the information pertaining to the Professors.

    Attributes
    ----------
    employee_code : int
        Primary Key of Professors table.

    name : str
        Name of professor.

    dept_id : int
        Foreign key referring to Department Table, denoting the department
        to which the professor belongs to

    activities : list
        List of activities belonging to this professor.

    """
    __tablename__ = 'professors'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    employee_code = Column(Integer(), primary_key=True)
    name = Column(String(255), index=True)
    dept_id = Column(Integer(), ForeignKey('department.dept_id'), nullable=False)

    created_on = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP"))
    last_updated = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        server_onupdate=FetchedValue())

    activities = relationship("ProfessorActivity", backref=backref('professor'),
                              order_by="ProfessorActivity.trans_id",
                              cascade="all, delete, delete-orphan")


class Authors(Base):
    """This class stores the information pertaining to the authors.

    Attributes
    ----------
    author_id : int
        Primary Key of Authors table.

    name : str
        Name of author.

    """
    __tablename__ = 'authors'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    author_id = Column(Integer(), primary_key=True)
    name = Column(String(255), index=True, nullable=False)

    created_on = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP"))
    last_updated = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        server_onupdate=FetchedValue())

    books = relationship("Books", backref="authors", secondary="book_has_authors")


class Books(Base):
    """This class stores the information pertaining to the books.

    Attributes
    ----------
    isbn_id : int
        Primary Key of Books table.

    name : str
        Name of book.

    quantity : int
        Number of copies of books available.

    dept_id : str
        Foreign key referring to Department Table, denoting the department
        to which the book belongs to

    book_items : list
        List of book_items belonging to this book.

    """
    __tablename__ = 'books'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    isbn_id = Column(Integer(), primary_key=True)
    name = Column(String(255), index=True, nullable=False)
    quantity = Column(Integer(), nullable=False)
    dept_id = Column(Integer(), ForeignKey('department.dept_id'), nullable=False)

    created_on = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP"))
    last_updated = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        server_onupdate=FetchedValue())

    book_items = relationship("BookItem", backref=backref('book'),
                              order_by="BookItem.bar_code",
                              cascade="all, delete, delete-orphan")


class BooksAuthor(Base):
    """This class stores the information pertaining to the BookAuthors-
    An Association table to reflect the many to many relationship between
    books and authors.

    Attributes
    ----------
    isbn_id : int
        Primary Key of BooksAuthor table, and also a foreign key denoting the book.

    author_id : int
        Primary Key of BooksAuthor table, and also a foreign key denoting the author.

    author : list
        List of authors belonging to this book.

    book : list
        List of books belonging to this author.

    """
    __tablename__ = 'book_has_authors'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    isbn_id = Column(Integer, ForeignKey("books.isbn_id"), primary_key=True)
    author_id = Column(Integer, ForeignKey("authors.author_id"), primary_key=True)

    created_on = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP"))
    last_updated = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        server_onupdate=FetchedValue())

    book = relationship("Books", backref=backref("author_associations",
                                                 cascade="all, delete, delete-orphan"))
    author = relationship("Authors", backref=backref("books_associations",
                                                     cascade="all, delete, delete-orphan"))


class Staffs(Base):
    """This class stores the information pertaining to the staffs.

    Attributes
    ----------
    staff_id : int
        Primary Key of Staffs table.

    name : str
        name of staff.

    student_activities : list
        List of student activities belonging to this staff.

    professor_activities : list
        List of professor activities belonging to this staff.

    """
    __tablename__ = 'staffs'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    staff_id = Column(Integer(), primary_key=True)
    name = Column(String(255), index=True, nullable=False)

    created_on = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP"))
    last_updated = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        server_onupdate=FetchedValue())

    student_activities = relationship("StudentActivity", backref=backref('staff'),
                                      order_by="StudentActivity.trans_id",
                                      cascade="all, delete, delete-orphan")
    professor_activities = relationship("ProfessorActivity", backref=backref('staff'),
                                        order_by="ProfessorActivity.trans_id",
                                        cascade="all, delete, delete-orphan")


class BookItem(Base):
    """This class stores the information pertaining to the book items.

    Attributes
    ----------
    bar_code : int
        Primary Key of BookItem table.

    dopur : DATE
        date of purchase.

    dopub : DATE
        date of publication.

    price : float
         price of book

    edition : float
        Edition of book

    status : ["Available", "Unavailable", "Lost"]
        Status of bookitem.

    tampered : Boolean
        set to true if while returning the book is tampered.

    isbn_id : int
        Foreign key referring to the Books table.

    """

    __tablename__ = 'book_item'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    bar_code = Column(Integer(), primary_key=True)
    # Date of Purchase
    dopur = Column(DATE(), nullable=False)
    # Date of Publication
    dopub = Column(DATE(), nullable=False)
    price = Column(Float(2), CheckConstraint('price >= 0.00'), nullable=False)
    edition = Column(Float(2))
    status = Column(Enum(BookStatus), default=BookStatus.AVAILABLE, nullable=False)
    tampered = Column(Boolean(), default=False)
    isbn_id = Column(Integer(), ForeignKey('books.isbn_id'), nullable=False)

    created_on = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP"))
    last_updated = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        server_onupdate=FetchedValue())


class StudentActivity(Base):
    """This class stores the information pertaining to the StudentActivity.

    Attributes
    ----------
    trans_id : int
        Primary Key of StudentActivity table.

    doi : DATE
        Date of issue.

    student_id : int
        Foreign key denoting the student's Id, from Students table.

    staff_id : list
        Foreign key denoting the staff's Id, from staff table who handled this transaction.

    """
    __tablename__ = 'student_activity'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    trans_id = Column(Integer(), primary_key=True)
    # Date of issue
    doi = Column(DATE(), nullable=False)
    student_id = Column(Integer(), ForeignKey('students.reg_id'), nullable=False)
    staff_id = Column(Integer(), ForeignKey('staffs.staff_id'), nullable=False)

    created_on = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP"))
    last_updated = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        server_onupdate=FetchedValue())

    book_items = relationship("BookItem", backref="student_activities", secondary="student_borrow")


class ProfessorActivity(Base):
    """This class stores the information pertaining to the ProfessorActivity.

    Attributes
    ----------
    trans_id : int
        Primary Key of ProfessorActivity table.

    doi : DATE
        Date of issue.

    student_id : int
        Foreign key denoting the professors's Id, from Professors table.

    staff_id : list
        Foreign key denoting the staff's Id, from staff table who handled this transaction.

    """
    __tablename__ = 'professor_activity'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    trans_id = Column(Integer(), primary_key=True)
    # Date of issue
    doi = Column(DATE(), nullable=False)
    professor_id = Column(Integer(), ForeignKey('professors.employee_code'), nullable=False)
    staff_id = Column(Integer(), ForeignKey('staffs.staff_id'), nullable=False)

    created_on = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP"))
    last_updated = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        server_onupdate=FetchedValue())

    book_items = relationship("BookItem", backref="professor_activities",
                              secondary="professor_borrow")


class StudentBorrow(Base):
    """This class stores the information pertaining to the StudentBorrow, which reflects the many
    to many relationship between student's transaction and book-items.

    Attributes
    ----------
    student_trans_id : int
        Primary Key of StudentBorrow table, also a foreign key denoting the student's transaction.

    book_bar_code_id : int
        Primary Key of StudentBorrow table, also a foreign key denoting the book_item.

    dd : DATE
        Due date.
    rd : DATE
        Date of return.

    student_activity : StudentActivity
        student activity in which this borrow with a specific book occurred.

    book_item : BookItem
        book item which occurred during this borrow.

    """
    __tablename__ = 'student_borrow'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    student_trans_id = Column(Integer, ForeignKey("student_activity.trans_id"), primary_key=True)
    book_bar_code_id = Column(Integer, ForeignKey("book_item.bar_code"), primary_key=True)
    due_date = Column(DATE(), nullable=False, default=date.today() + timedelta(15))
    return_date = Column(DATE())

    created_on = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP"))
    last_updated = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        server_onupdate=FetchedValue())

    student_activity = relationship("StudentActivity",
                                    backref=backref("book_item_associations",
                                                    cascade="all, delete, delete-orphan"))
    book_item = relationship("BookItem", backref=backref("student_activity_associations",
                                                         cascade="all, delete, delete-orphan"))


class ProfessorBorrow(Base):
    """This class stores the information pertaining to the ProfessorBorrow, which reflects the many
    to many relationship between professor's transaction and book-items.

    Attributes
    ----------
    professor_trans_id : int
        Primary Key of ProfessorBorrow table, also a foreign key
        denoting the professor's transaction.

    book_bar_code_id : int
        Primary Key of StudentBorrow table, also a foreign key denoting the book_item.

    dd : DATE
        Due date.
    rd : DATE
        Date of return.

    professor_activity : StudentActivity
        professor activity in which this borrow with a specific book occurred.

    book_item : BookItem
        book item which occurred during this borrow.

    """

    __tablename__ = 'professor_borrow'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    professor_trans_id = Column(Integer, ForeignKey("professor_activity.trans_id"),
                                primary_key=True)
    book_bar_code_id = Column(Integer, ForeignKey("book_item.bar_code"),
                              primary_key=True)
    # Due Date
    due_date = Column(DATE(), nullable=False, default=date.today() + timedelta(15))
    # Return Date
    return_date = Column(DATE())

    created_on = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP"))
    last_updated = Column(
        TIMESTAMP,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        server_onupdate=FetchedValue())

    professor_activity = relationship("ProfessorActivity",
                                      backref=backref("book_item_associations",
                                                      cascade="all, delete, delete-orphan"))
    book_item = relationship("BookItem", backref=backref("professor_activity_associations",
                                                         cascade="all, delete, delete-orphan"))
