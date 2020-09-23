# -*- coding: utf-8 -*-
""" Module for populating the database with some random data

This script contains all the functions to populate the database using
orm_queries classes, it contains the following functions

    * populate
    * main

This script requires that the following packages be installed within the Python
environment you are running this script in.

    * sqlalchemy - Package used to connect to a database and do SQL operations using orm_queries

"""

# Standard import
import random
from datetime import date, timedelta

# External import
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# User Import
from library.orm_queries.models import Staffs, Department, \
    Students, Professors, Books, BookItem,\
    Base, Authors, BooksAuthor


__author__ = 'praveen@gyandata.com'

# pylint: disable=too-few-public-methods


def populate(session):
    """
    Function to populate the database

    Parameters
    ----------
    session: Session
            The session object that will be used to populate the database
    """

    # Adding Staffs
    staff1 = Staffs(name="Staff-1")
    staff2 = Staffs(name="Staff-2")
    staff3 = Staffs(name="Staff-3")

    # Adding to session
    session.add_all([staff1, staff2, staff3])
    session.flush()

    # Adding Departments
    departments = [Department(name="Mechanical"),
                   Department(name="Computer"),
                   Department(name="Electrical")]

    # Adding to session
    session.add_all(departments)
    session.flush()

    # Adding Students, professors, books, authors and book-items for all departments
    for department in departments:
        for i in range(10):

            student = Students(name="student" + str(department.name) + str(i),
                               doj=date.today() - timedelta(random.randint(30, 600)),
                               department=department)
            session.add(student)
            session.commit()

        for i in range(3):

            professor = Professors(name="professor" + str(department.name) + str(i),
                                   department=department)
            session.add(professor)
            session.commit()

        for i in range(10):

            # pylint: disable=no-member

            book = Books(name="book" + str(department.name) + str(i), quantity=2,
                         department=department)
            author = Authors(name="Author" + str(department.name) + str(i))
            book_author = BooksAuthor()
            book_1 = BookItem(dopur=date.today() - timedelta(random.randint(30, 600)),
                              dopub=date.today() - timedelta(random.randint(30, 600)),
                              price=round((random.random() * 10000), 2),
                              edition=1.0, book=book)
            book_2 = BookItem(dopur=date.today() - timedelta(random.randint(30, 600)),
                              dopub=date.today() - timedelta(random.randint(30, 600)),
                              price=round((random.random() * 10000), 2),
                              edition=2.0, book=book)
            session.add_all([book, author, book_author, book_1, book_2])
            book_author.book = book
            author.books.append(book_author)
            session.commit()


def main():
    """ The main function to initialize engines and call necessary functions"""

    # pylint: disable=no-member
    # pylint: disable=invalid-name

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
