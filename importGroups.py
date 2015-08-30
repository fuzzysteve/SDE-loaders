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

invGroups = Table('invGroups',metadata,
				Column('groupID',Integer,primary_key=True, autoincrement=False),
				Column('categoryID',Integer),
				Column('groupName',String(100)),
				Column('iconID',BigInteger),
				Column('useBasePrice',Boolean),
				Column('anchored',Boolean),
				Column('anchorable',Boolean),
				Column('fittableNonSingleton',Boolean),
				Column('published',Boolean),
				)
Index('invTypes_categoryid',invGroups.c.categoryID)

trnTranslations = Table('trnTranslations',metadata,
						Column('tcID',Integer,primary_key=True,autoincrement=False),
						Column('keyID',Integer,primary_key=True,autoincrement=False),
						Column('languageID',String,primary_key=True,autoincrement=False),
						Column('text',Text)
);

metadata.create_all(engine,checkfirst=True)

print "opening Yaml"
with open(sourcePath+'groupIDs.yaml','r') as yamlstream:
    print "importing"
    trans = connection.begin()
    groupids=yaml.load(yamlstream,Loader=yaml.CSafeLoader)
    print "Yaml Processed into memory"
    for groupid in groupids:
        connection.execute(invGroups.insert(),
                           groupID=groupid,
                           categoryID=groupids[groupid].get('categoryID',0),
                           groupName=groupids[groupid].get('name',{}).get('en','').decode('utf-8'),
						   iconID=groupids[groupid].get('iconID'),
						   useBasePrice=groupids[groupid].get('useBasePrice'),
                           anchored=groupids[groupid].get('anchored',0),
                           anchorable=groupids[groupid].get('anchorable',0),
                           fittableNonSingleton=groupids[groupid].get('fittableNonSingleton',0),
						   published=groupids[groupid].get('published',0))
        if (groupids[groupid].has_key('name')):
            for lang in groupids[groupid]['name']:
                connection.execute(trnTranslations.insert(),tcID=7,keyID=groupid,languageID=lang,text=groupids[groupid]['name'][lang].decode('utf-8'));
trans.commit()
