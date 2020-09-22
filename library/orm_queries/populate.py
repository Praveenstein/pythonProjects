# -*- coding: utf-8 -*-
""" Module for populating the database with some random data

This script contains all the functions to populate the database using
orm_queries classes, it contains the following functions

    * populate
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


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import random
from library.orm_queries.models import *

__author__ = 'praveen@gyandata.com'


def populate(session):

    # Adding Staffs

    staff1 = Staffs(name="Staff-1")
    staff2 = Staffs(name="Staff-2")
    staff3 = Staffs(name="Staff-3")
    try:
        session.add_all([staff1, staff2, staff3])
        session.flush()
    except Exception as err:
        session.rollback()
        print(err)

    # Adding Departments

    mechanical = Department(name="Mechanical")
    cs = Department(name="Computer")
    ee = Department(name="Electrical")
    departments = [mechanical, cs, ee]
    try:
        session.add_all(departments)
        session.flush()
    except Exception as err:
        session.rollback()
        print(err)

    # Adding Students, professors, books, authors and book-items for all departments

    for department in departments:
        for i in range(10):
            try:
                student = Students(name="student" + str(department.name) + str(i),
                                   doj=date.today() - timedelta(random.randint(30, 600)), department=department)
                session.add(student)
                session.commit()
            except Exception as err:
                session.rollback()
                print(err)

        for i in range(3):
            try:
                professor = Professors(name="professor" + str(department.name) + str(i), department=department)
                session.add(professor)
                session.commit()
            except Exception as err:
                session.rollback()
                print(err)

        for i in range(10):
            try:

                book = Books(name="book" + str(department.name) + str(i), quantity=2, department=department)
                author = Authors(name="Author" + str(department.name) + str(i))
                ba = BooksAuthor()
                book_1 = BookItem(dopur=date.today() - timedelta(random.randint(30, 600)),
                                  dopub=date.today() - timedelta(random.randint(30, 600)),
                                  price=round((random.random() * 10000), 2),
                                  edition=1.0, book=book)
                book_2 = BookItem(dopur=date.today() - timedelta(random.randint(30, 600)),
                                  dopub=date.today() - timedelta(random.randint(30, 600)),
                                  price=round((random.random() * 10000), 2),
                                  edition=2.0, book=book)
                session.add_all([book, author, ba, book_1, book_2])
                ba.book = book
                author.books.append(ba)
                session.commit()
            except Exception as err:
                session.rollback()
                print(err)


def main():

    url = "mysql+pymysql://root:nebula@localhost/library1?charset=utf8mb4"
    engine = create_engine(url)

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)

    pop_session = Session()

    populate(pop_session)

    populate(pop_session)

    pop_session.close()


if __name__ == '__main__':
    main()
