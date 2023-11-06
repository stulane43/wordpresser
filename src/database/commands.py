import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

import logging

from . import models
from .wpdb import engine

def create_tables(create: bool):
    '''
    Creates tables from models.py
    '''
    try:
        if create:
            models.Base.metadata.create_all(bind=engine)
    except Exception as e:
        logging.error("Error: {}".format(e))
        
def read(query: str):
    '''
    Reads database using pandas with a supplied query and db engine
    '''
    try:
        data = pd.read_sql(query, engine)
        return data
    except Exception as e:
        logging.error("commands.py - read: [{}]".format(e))
        
def insert(table: str, df: pd.DataFrame):
    '''
    Insert data into db table
    '''
    try:
        df.to_sql(table, engine, if_exists="append", index=False)
    except Exception as e:
        logging.error("commands.py - insert: [{}]".format(e))
        
def temp_insert(table: str, df: pd.DataFrame):
    '''
    Insert data into db table
    '''
    try:
        df.to_sql(table, engine, if_exists="replace", index=False)
    except Exception as e:
        logging.error("commands.py - insert: [{}]".format(e))
        
def call_stored_procs():
    '''
    Calls Stored Procedures in app_discovery
    '''
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        logging.debug("Updating WordPresser Tables")
        sql = text('CALL UpdateWordpress();')
        session.execute(sql)
        session.commit()
    except Exception as e:
        logging.error("commands.py - call_stored_procs: [{}]".format(e))
    finally:
        session.close()