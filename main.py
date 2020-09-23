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
from library.ORM.models import Base
from library.POPULATE.populate import populate
from library.QUERY.queries import log, test


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

    # Creating a session to populate the database
    pop_session = Session()

    # Populating the database
    populate(pop_session)

    # Closing the session
    pop_session.close()

    # Creating logger
    log()

    # Doing some student transactions and displaying the impact and other details
    test(Session)

    # Deleting all tables
    Base.metadata.drop_all(engine)


if __name__ == '__main__':
    main()
