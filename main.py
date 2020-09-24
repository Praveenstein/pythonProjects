# -*- coding: utf-8 -*-
""" Main module for populating the database and performing queries

This script requires that the following packages be installed within the Python
environment you are running this script in.

    * sqlalchemy - Package used to connect to a database and do SQL operations using orm_queries
"""

# External import
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# User Import
from library.orm.models import Base
from library.populate.populate_db import populate
from library.query.queries import basic_trans, impact_analysis, test_tamper


__author__ = 'praveen@gyandata.com'


def main():
    """Main Function to populate the database and perform queries"""

    # pylint: disable=no-member
    # pylint: disable=invalid-name

    # Creating engine to connect to Mysql database
    url = "mysql+pymysql://root:nebula@localhost/library1?charset=utf8mb4"
    engine = create_engine(url)

    # Creating all the tables
    Base.metadata.create_all(engine)

    # creating a session factory
    Session = sessionmaker(bind=engine)

    # Populating the database, # Giving a new session as parameter
    populate(Session())

    # Calling the basic transaction to do some issues, passing the
    # Session factory as parameter
    basic_trans(Session)

    # Doing some student transactions and displaying the impact and other details,
    # And passing the Session factory as parameter
    test_tamper(Session)

    # Calling impact analysis to issue to books and check the impact
    # On Computer science department
    # And passing the session factory as parameter
    impact_analysis(Session)

    # Deleting all tables
    Base.metadata.drop_all(engine)


if __name__ == '__main__':
    main()
