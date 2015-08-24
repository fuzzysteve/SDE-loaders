# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import pyodbc
import yaml
import pprint
from sqlalchemy import create_engine, Column, MetaData, Table, Index, select
from sqlalchemy import Integer, String, Text, Float, Boolean, BigInteger, Numeric, SmallInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

def make_session(in_engine):
    engine = in_engine
    Session = sessionmaker(bind=engine)
    return Session(), engine

def pull_data(from_db, to_db, tables):
    source, sengine = make_session(from_db)
    destination, dengine = make_session(to_db)
    meta = MetaData()
    for table_name in tables:
        print 'Processing', table_name
        print 'Pulling schema from source server'
        if table_name=='mapCelestialStatistics':
            table = Table(table_name, meta, Column('pressure',BigInteger),Column('radius',BigInteger),autoload=True,autoload_with=sengine)
        else:
            table = Table(table_name, meta, autoload=True,autoload_with=sengine)
        print 'Creating table on destination server'
        table.drop(dengine,checkfirst=True)
        table.create(dengine,checkfirst=True)
        ins = table.insert()
        s = select([table])
        result = source.execute(s)
        print 'Transferring records'
        while True:
            l = result.fetchmany(1000)
            if len(l) == 0:
                break
            destination.execute(ins, l) 
        print 'Committing changes'
        destination.commit()

        
        
        
def create_indexes(from_db, to_db, tables):

def quick_mapper(table):
    Base = declarative_base()
    class GenericMapper(Base):
        __table__ = table
    return GenericMapper

if __name__ == '__main__':
    print "connecting to MSSQL DB"
    engine = create_engine('mssql+pyodbc://ebs')
    connection = engine.connect()
    print "connecting to SQLLite DB"
    sqliteengine = create_engine('sqlite+pysqlite:///universeDataDx.db')
    sqliteconnection = sqliteengine.connect()
    metadata = MetaData()
    metadata.reflect(sqliteengine)
    tablelist=metadata.tables.keys()
    pull_data(sqliteengine,engine,tablelist)