# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import pyodbc
import yaml
import pprint
import sqlalchemy

print "connecting to DB"
engine = sqlalchemy.create_engine('mssql+pyodbc://ebs')
connection = engine.connect()



metadata = sqlalchemy.MetaData()
invTypes = sqlalchemy.Table('invTypes',metadata,autoload=True, autoload_with=engine);
trnTranslations = sqlalchemy.Table('trnTranslations',metadata,autoload=True, autoload_with=engine);

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
        if (typeids[typeid].has_key('name')):
            for lang in typeids[typeid]['name']:
                connection.execute(trnTranslations.insert(),tcID=8,keyID=typeid,languageID=lang,text=typeids[typeid]['name'][lang].decode('utf-8'));
        if (typeids[typeid].has_key('description')):
            for lang in typeids[typeid]['description']:
                connection.execute(trnTranslations.insert(),tcID=33,keyID=typeid,languageID=lang,text=typeids[typeid]['description'][lang].decode('utf-8'));
trans.commit()
