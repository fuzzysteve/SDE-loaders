# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import pyodbc
import yaml
import pprint
from sqlalchemy import create_engine, Column, MetaData, Table, Index
from sqlalchemy import Integer, String, Text, Float, Boolean, BigInteger, Numeric, SmallInteger,Unicode,UnicodeText


print "connecting to DB"
engine = create_engine('mssql+pyodbc://ebs')
connection = engine.connect()



metadata = MetaData()

print "Setting up Tables"

invTypes = Table('invTypes',metadata,
                Column('typeID',BigInteger,primary_key=True, autoincrement=False),
                Column('groupID',Integer),
                Column('typeName',String(100)),
                Column('description',Text),
                Column('mass',Float),
                Column('volume',Float),
                Column('capacity',Float),
                Column('portionSize',Integer),
                Column('raceID',SmallInteger),
                Column('basePrice',Numeric(scale=4,precision=19)),
                Column('published',Boolean),
                Column('marketGroupID',BigInteger),
                Column('iconID',BigInteger),
                Column('soundID',BigInteger)
                )
Index('invTypes_groupid',invTypes.c.groupID)

trnTranslations = Table('trnTranslations',metadata,
                        Column('tcID',Integer,autoincrement=False),
                        Column('keyID',Integer,autoincrement=False),
                        Column('languageID',Unicode,autoincrement=False),
                        Column('text',UnicodeText)
)
certMasteries = Table('certMasteries',metadata,
                    Column('typeID',Integer),
                    Column('masteryLevel',Integer),
                    Column('certID',Integer))
invTraits = Table('invTraits',metadata,
                    Column('traitID',Integer,primary_key=True),
                    Column('typeID',Integer),
                    Column('skillID',Integer),
                    Column('bonus',Float),
                    Column('bonusText',Text),
                    Column('unitID',Integer))
                

metadata.create_all(engine,checkfirst=True)

print "opening Yaml"
with open('typeIDs.yaml','r') as yamlstream:
    print "importing"
    trans = connection.begin()
    typeids=yaml.load(yamlstream,Loader=yaml.CSafeLoader)
    print "Yaml Processed into memory"
    for typeid in typeids:
        connection.execute(invTypes.insert(),
                           typeID=typeid,
                           groupID=typeids[typeid].get('groupID',0),
                           typeName=typeids[typeid].get('name',{}).get('en','').decode('utf-8'),
                           description=typeids[typeid].get('description',{}).get('en','').decode('utf-8'),
                           mass=typeids[typeid].get('mass',0),
                           volume=typeids[typeid].get('volume',0),
                           capacity=typeids[typeid].get('capacity',0),
                           portionSize=typeids[typeid].get('portionSize'),
                           raceID=typeids[typeid].get('raceID'),
                           basePrice=typeids[typeid].get('basePrice'),
                           published=typeids[typeid].get('published',0),
                           marketGroupID=typeids[typeid].get('marketGroupID'),
                           iconID=typeids[typeid].get('iconID'),
                           soundID=typeids[typeid].get('soundID'))
        if  typeids[typeid].has_key("masteries"):
            for level in typeids[typeid]["masteries"]:
                for cert in typeids[typeid]["masteries"][level]:
                    connection.execute(certMasteries.insert(),
                                        typeID=typeid,
                                        masteryLevel=level,
                                        certID=cert)
        if (typeids[typeid].has_key('name')):
            for lang in typeids[typeid]['name']:
                connection.execute(trnTranslations.insert(),tcID=8,keyID=typeid,languageID=lang.decode('utf-8'),text=typeids[typeid]['name'][lang].decode('utf-8'))
        if (typeids[typeid].has_key('description')):
            for lang in typeids[typeid]['description']:
                connection.execute(trnTranslations.insert(),tcID=33,keyID=typeid,languageID=lang.decode('utf-8'),text=typeids[typeid]['description'][lang].decode('utf-8'))
        if (typeids[typeid].has_key('traits')):
            for skill in typeids[typeid]['traits']:
                for trait in typeids[typeid]['traits'][skill]:
                    result=connection.execute(invTraits.insert(),
                                        typeID=typeid,
                                        skillID=skill,
                                        bonus=typeids[typeid]['traits'][skill][trait].get('bonus'),
                                        bonusText=typeids[typeid]['traits'][skill][trait].get('bonusText',{}).get('en',''),
                                        unitID=typeids[typeid]['traits'][skill][trait].get('unitID'))
                    traitid=result.inserted_primary_key
                    for languageid in typeids[typeid]['traits'][skill][trait].get('bonusText',{}):
                        connection.execute(trnTranslations.insert(),tcID=1001,keyID=traitid[0],languageID=languageid.decode('utf-8'),text=typeids[typeid]['traits'][skill][trait]['bonusText'][languageid].decode('utf-8'))
trans.commit()
