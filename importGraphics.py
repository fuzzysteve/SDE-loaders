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

eveGraphics = Table('eveGraphics',metadata,
                Column('graphicID',Integer,primary_key=True, autoincrement=False),
                Column('sofFactionName',String(100)),
                Column('graphicFile',String(100)),
                Column('sofHullName',String(100)),
                Column('sofRaceName',String(100)),
                Column('description',Text)
                )


metadata.create_all(engine,checkfirst=True)

print "opening Yaml"
with open(sourcePath+'graphicIDs.yaml','r') as yamlstream:
    print "importing"
    trans = connection.begin()
    graphics=yaml.load(yamlstream,Loader=yaml.CSafeLoader)
    print "Yaml Processed into memory"
    for graphic in graphics:
        connection.execute(eveGraphics.insert(),
                           graphicID=graphic,
                           sofFactionName=graphics[graphic].get('sofFactionName',''),
                           graphicFile=graphics[graphic].get('graphicFile',''),
                           sofHullName=graphics[graphic].get('sofHullName',''),
                           sofRaceName=graphics[graphic].get('sofRaceName',''),
                           description=graphics[graphic].get('description',''))
trans.commit()
