# -*- coding: utf-8 -*-
""" Module for creating Engine and session maker factory

This script requires that the following packages be installed within the Python
environment you are running this script in.

    * sqlalchemy - Package used to connect to a database and do SQL operations using orm_queries
    * json - Package used to parse json files
"""

# Standard Imports
import json

# External Imports
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker


def create_engine():
    """
    Function used to read the configuration file and create engine
    :return: engine
    """
    with open("configs\\engine_config.json") as file:
        data = json.load(file)
    engine = engine_from_config(data)
    return engine


ENGINE = create_engine()
SESSION_FACTORY = sessionmaker(bind=ENGINE)
