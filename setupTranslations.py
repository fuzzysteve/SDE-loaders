# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import pyodbc
import yaml
import pprint
from sqlalchemy import create_engine, Column, MetaData, Table, Index
from sqlalchemy import Integer, String, Text, Float, Boolean, BigInteger, Numeric, SmallInteger,Unicode,UnicodeText
import csv


import ConfigParser, os
fileLocation = os.path.dirname(os.path.realpath(__file__))
inifile=fileLocation+'/sdeloader.cfg'
config = ConfigParser.ConfigParser()
config.read(inifile)
destination=config.get('Database','destination')
sourcePath=config.get('Files','sourcePath')

print "connecting to DB"
engine = create_engine(destination)
connection = engine.connect()



metadata = MetaData()

print "Setting up Tables"

trnTranslationColumns = Table('trnTranslationColumns',metadata,
                        Column('tcGroupID',Integer,autoincrement=False),
                        Column('tcID',Integer,autoincrement=False),
                        Column('tableName',Unicode(256),autoincrement=False),
                        Column('columnName',Unicode(128)),
                        Column('masterID',Unicode(128))
)
               

metadata.create_all(engine,checkfirst=True)


trans = connection.begin()

with open(sourcePath+'trnTranslationColumns.csv','rb') as csvfile:
    filereader = csv.reader(csvfile,dialect='excel')
    for row in filereader:
        connection.execute(trnTranslationColumns.insert(),tcGroupID=row[0],tcID=row[1],tableName=row[2],columnName=row[3],masterID=row[4])
trans.commit()
