# -*- coding: utf-8 -*-
""" Main module for populating the database and performing queries

This script requires that the following packages be installed within the Python
environment you are running this script in.

    * sqlalchemy - Package used to connect to a database and do SQL operations using orm_queries
"""

# User Import
from library.connections.get_connection import ENGINE
from library.orm.models import Base
from library.populate.populate_db import populate
from library.query.queries import basic_trans, impact_analysis,\
    test_tamper


__author__ = 'praveen@gyandata.com'


def main():
    """Main Function to populate the database and perform queries"""

    # Creating all the tables
    Base.metadata.create_all(ENGINE)

    # Populating the database, # Giving a new session as parameter
    populate()

    # Calling the basic transaction to do some issues, passing the
    # Session factory as parameter
    basic_trans()

    # Doing some student transactions and displaying the impact and other details,
    # And passing the Session factory as parameter
    test_tamper()

    # Calling impact analysis to issue to books and check the impact
    # On Computer science department
    # And passing the session factory as parameter
    impact_analysis()

    # Deleting all tables
    Base.metadata.drop_all(ENGINE)


if __name__ == '__main__':
    main()
