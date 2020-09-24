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
from library.orm.models import Staffs, Department, \
    Students, Professors, Books, BookItem,\
    Base, Authors


__author__ = 'praveen@gyandata.com'


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

        # For every department, books, students and professors are created
        for i in range(10):

            # Creating 10 students per department
            student = Students(name="student" + str(department.name) + str(i),
                               doj=date.today() - timedelta(random.randint(30, 600)),
                               department=department)
            session.add(student)
            session.commit()

        for i in range(3):

            # Creating 3 professor per department
            professor = Professors(name="professor" + str(department.name) + str(i),
                                   department=department)
            session.add(professor)
            session.commit()

        for i in range(10):

            # Creating 10 books and one author for every book
            book = Books(name="book" + str(department.name) + str(i), quantity=2,
                         department=department)
            author = Authors(name="Author" + str(department.name) + str(i))
            book_1 = BookItem(dopur=date.today() - timedelta(random.randint(30, 600)),
                              dopub=date.today() - timedelta(random.randint(30, 600)),
                              price=round((random.random() * 10000), 2),
                              edition=1.0, book=book)
            book_2 = BookItem(dopur=date.today() - timedelta(random.randint(30, 600)),
                              dopub=date.today() - timedelta(random.randint(30, 600)),
                              price=round((random.random() * 10000), 2),
                              edition=2.0, book=book)
            session.add_all([book, author, book_1, book_2])
            author.books.append(book)
            session.commit()

    # Closing the session
    session.close()


def main():
    """ The main function to initialize engines and call necessary functions"""

    url = "mysql+pymysql://root:nebula@localhost/library1?charset=utf8mb4"
    engine = create_engine(url)

    # Creating all tables in the database
    Base.metadata.create_all(engine)

    # Creating a session factory
    Session = sessionmaker(bind=engine)

    # Creating a new session to populate the database
    pop_session = Session()

    # calling populate function to populate the database
    populate(pop_session)


if __name__ == '__main__':
    main()
