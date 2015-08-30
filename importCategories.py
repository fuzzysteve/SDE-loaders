# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import pyodbc
import yaml
import pprint
from sqlalchemy import create_engine, Column, MetaData, Table, Index
from sqlalchemy import Integer, String, Text, Float, Boolean, BigInteger, Numeric, SmallInteger

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

invCategories = Table('invCategories',metadata,
				Column('categoryID',Integer,primary_key=True, autoincrement=False),
				Column('categoryName',String(100)),
				Column('iconID',BigInteger),
				Column('published',Boolean),
				)

trnTranslations = Table('trnTranslations',metadata,
						Column('tcID',Integer,primary_key=True,autoincrement=False),
						Column('keyID',Integer,primary_key=True,autoincrement=False),
						Column('languageID',String,primary_key=True,autoincrement=False),
						Column('text',Text)
);

metadata.create_all(engine,checkfirst=True)

print "opening Yaml"
with open(sourcePath+'categoryIDs.yaml','r') as yamlstream:
    print "importing"
    trans = connection.begin()
    categoryids=yaml.load(yamlstream,Loader=yaml.CSafeLoader)
    print "Yaml Processed into memory"
    for categoryid in categoryids:
        connection.execute(invCategories.insert(),
                           categoryID=categoryid,
                           categoryName=categoryids[categoryid].get('name',{}).get('en','').decode('utf-8'),
						   iconID=categoryids[categoryid].get('iconID'),
						   published=categoryids[categoryid].get('published',0))
        if (categoryids[categoryid].has_key('name')):
            for lang in categoryids[categoryid]['name']:
                connection.execute(trnTranslations.insert(),tcID=6,keyID=categoryid,languageID=lang,text=categoryids[categoryid]['name'][lang].decode('utf-8'));
trans.commit()
