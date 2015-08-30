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

from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import REAL

# redefining REAL datatypes to be a double precision float. Might be a touch execessive, but deals with a mapping bug,
# forcing a double, rather than a float (which is too small)
@compiles(REAL, "mssql")
def compile_real_mssql(type_, compiler, **kw):
    return "FLOAT(53)"







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
        elif table_name=='mapLandmarks':
            table = Table(table_name, meta, Column('description',Text),autoload=True,autoload_with=sengine)
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



def quick_mapper(table):
    Base = declarative_base()
    class GenericMapper(Base):
        __table__ = table
    return GenericMapper

if __name__ == '__main__':
    import ConfigParser, os
    fileLocation = os.path.dirname(os.path.realpath(__file__))
    inifile=fileLocation+'/sdeloader.cfg'
    config = ConfigParser.ConfigParser()
    config.read(inifile)
    destination=config.get('Database','destination')
    sqlitedriver=config.get('Database','sqlitedriver')
    sourcePath=config.get('Files','sourcePath')
    print "connecting to MSSQL DB"
    engine = create_engine(destination)
    connection = engine.connect()
    print "connecting to SQLLite DB"
    sqliteengine = create_engine(sqlitedriver+sourcePath+'universeDataDx.db')
    sqliteconnection = sqliteengine.connect()
    metadata = MetaData()
    metadata.reflect(sqliteengine)
    tablelist=metadata.tables.keys()
    pull_data(sqliteengine,engine,tablelist)