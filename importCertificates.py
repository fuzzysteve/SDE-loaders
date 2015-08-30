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

certCerts = Table('certCerts',metadata,
                Column('certID',Integer,primary_key=True, autoincrement=False),
                Column('description',Text),
                Column('groupID',Integer),
                Column('name',String(255))
                )
                
certSkills = Table('certSkills',metadata,
                Column('certID',Integer,index=True),
                Column('skillID',Integer),
                Column('certLevelInt',Integer),
                Column('skillLevel',Integer),
                Column('certLevelText',String(8))
                )


metadata.create_all(engine,checkfirst=True)

skillmap={"basic":0,"standard":1,"improved":2,"advanced":3,"elite":4}

print "opening Yaml"
with open(sourcePath+'certificates.yaml','r') as yamlstream:
    print "importing"
    trans = connection.begin()
    certificates=yaml.load(yamlstream,Loader=yaml.CSafeLoader)
    print "Yaml Processed into memory"
    for certificate in certificates:
        connection.execute(certCerts.insert(),
                           certID=certificate,
                           name=certificates[certificate].get('name',''),
                           description=certificates[certificate].get('description',''),
                           groupID=certificates[certificate].get('groupID'))
        for skill in certificates[certificate]['skillTypes']:
            for skillLevel in certificates[certificate]['skillTypes'][skill]:
                connection.execute(certSkills.insert(),
                                    certID=certificate,
                                    skillID=skill,
                                    certLevelInt=skillmap[skillLevel],
                                    certLevelText=skillLevel,
                                    skillLevel=certificates[certificate]['skillTypes'][skill][skillLevel]
                                    )
trans.commit()
