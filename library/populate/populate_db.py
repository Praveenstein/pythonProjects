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
from contextlib import contextmanager
import json
import logging
import logging.config

# User Import
from library.orm.models import Staffs, Department, \
    Students, Professors, Books, BookItem,\
    Base, Authors
from library.connections.get_connection import Session, config_session, engine


__author__ = 'praveen@gyandata.com'

POP_LOGGER = logging.getLogger(__name__)


def config_log_pop():
    with open('D:\\Profession\\Intern\\Assignments\\master_repo\\'
              'pythonProjects\\configs\\pop_log.json', 'r') as file:
        config = json.load(file)

    logging.config.dictConfig(config)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except AssertionError as err:
        POP_LOGGER.error(err)
    except AttributeError as err:
        session.rollback()
        POP_LOGGER.error(err)
    finally:
        session.close()


def populate():
    """
    Function to populate the database
    """
    with session_scope() as session:
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


def main():
    """ The main function to initialize engines and call necessary functions"""

    # Creating all tables in the database
    Base.metadata.create_all(engine)

    # Configure the logger
    config_log_pop()

    # Configure the session
    config_session()

    # calling populate function to populate the database
    populate()


if __name__ == '__main__':
    main()
