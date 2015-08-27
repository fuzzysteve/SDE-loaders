# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import pyodbc
import yaml
import pprint
from sqlalchemy import create_engine, Column, MetaData, Table, Index
from sqlalchemy import Integer, String, Text, Float, Boolean, BigInteger, Numeric, SmallInteger


print "connecting to DB"
engine = create_engine('mssql+pyodbc://ebs')
connection = engine.connect()



metadata = MetaData()

print "Setting up Tables"

skinLicense = Table('skinLicense',metadata,
                Column('licenseTypeID',Integer,primary_key=True, autoincrement=False),
                Column('duration',Integer),
                Column('skinID',Integer)
                )
skinMaterials = Table('skinMaterials',metadata,
                Column('skinMaterialID',Integer,primary_key=True, autoincrement=False),
                Column('displayNameID',Integer),
                Column('materialSetID',Integer)
                )

skins_table = Table('skins',metadata,
                Column('skinID',Integer,primary_key=True, autoincrement=False),
                Column('internalName',String(70)),
                Column('skinMaterialID',Integer)
                )
skinShip = Table('skinShip',metadata,
                Column('skinID',Integer,index=True),
                Column('typeID',Integer,index=True)
                )            
                
                
metadata.create_all(engine,checkfirst=True)
trans = connection.begin()
print "opening Yaml1"
with open('skins.yaml','r') as yamlstream:
    print "importing"
    skins=yaml.load(yamlstream,Loader=yaml.CSafeLoader)
    print "Yaml Processed into memory"
    for skinid in skins:
        connection.execute(skins_table.insert(),
                           skinID=skinid,
                           internalName=skins[skinid].get('internalName',''),
                           skinMaterialID=skins[skinid].get('skinMaterialID',''))
        for ship in skins[skinid]['types']:
            connection.execute(skinShip.insert(),
                            licenseTypeID=skinid,
                            typeID=ship)


print "opening Yaml2"
with open('skinLicenses.yaml','r') as yamlstream:
    print "importing"
    skinlicenses=yaml.load(yamlstream,Loader=yaml.CSafeLoader)
    print "Yaml Processed into memory"
    for licenseid in skinlicenses:
        connection.execute(skinLicense.insert(),
                            licenseTypeID=licenseid,
                            duration=skinlicenses[licenseid]['duration'],
                            skinID=skinlicenses[licenseid]['skinID'])
print "opening Yaml3"
with open('skinMaterials.yaml','r') as yamlstream:
    print "importing"
    skinmaterials=yaml.load(yamlstream,Loader=yaml.CSafeLoader)
    print "Yaml Processed into memory"
    for materialid in skinmaterials:
        connection.execute(skinMaterials.insert(),
                            skinMaterialID=materialid,
                            displayNameID=skinmaterials[materialid]['displayNameID'],
                            materialSetID=skinmaterials[materialid]['materialSetID']
                            )

trans.commit()
