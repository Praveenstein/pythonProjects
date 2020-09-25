# -*- coding: utf-8 -*-
""" Main module for creating engines and session factory

This script requires that the following packages be installed within the Python
environment you are running this script in.

    * sqlalchemy - Package used to connect to a database and do SQL operations using orm_queries
"""

# External import
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

url = "mysql+pymysql://root:nebula@localhost/library1?charset=utf8mb4"
engine = create_engine(url)

# Creating a session factory
Session = sessionmaker()


def config_session():
    """
    This function is used to configure the session factory to connect to the engine
    :return:
    """
    Session.configure(bind=engine)
