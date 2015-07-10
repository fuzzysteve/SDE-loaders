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
    typeids=yaml.load(yamlstream,Loader =yaml.CLoader)
    print "Yaml Processed into memory"
    for typeid in typeids:
        print typeid
        connection.execute(invTypes.insert(),
                           typeID=typeid,
                           groupID=typeids[typeid]['groupID'] if typeids[typeid].has_key('groupID') else 0,
                           typeName=typeids[typeid]['name']['en'] if (typeids[typeid].has_key('name') and typeids[typeid]['name'].has_key('en')) else '',
                           description=typeids[typeid]['description']['en'] if (typeids[typeid].has_key('description') and typeids[typeid]['description'].has_key('en')) else '',
                           mass=typeids[typeid]['mass'] if typeids[typeid].has_key('mass') else 0,
                           volume=typeids[typeid]['volume'] if typeids[typeid].has_key('volume') else 0,
                           capacity=typeids[typeid]['capacity'] if typeids[typeid].has_key('capacity') else 0,
                           portionSize=typeids[typeid]['portionSize'] if typeids[typeid].has_key('portionSize') else 0,
                           raceID=typeids[typeid]['raceID'] if typeids[typeid].has_key('raceID') else 0,
                           basePrice=typeids[typeid]['basePrice'] if typeids[typeid].has_key('basePrice') else 0,
                           published=typeids[typeid]['published'] if typeids[typeid].has_key('published') else 0,
                           marketGroupID=typeids[typeid]['marketGroupID'] if typeids[typeid].has_key('marketGroupID') else 0,
                           iconID=typeids[typeid]['iconID'] if typeids[typeid].has_key('iconID') else 0,
                           soundID=typeids[typeid]['soundID'] if typeids[typeid].has_key('soundID') else 0)
        if (typeids[typeid].has_key('name')):
            for lang in typeids[typeid]['name']:
                connection.execute(trnTranslations.insert(),tcID=8,keyID=typeid,languageID=lang,text=typeids[typeid]['name'][lang]);
        if (typeids[typeid].has_key('description')):
            for lang in typeids[typeid]['description']:
                connection.execute(trnTranslations.insert(),tcID=33,keyID=typeid,languageID=lang,text=typeids[typeid]['description'][lang]);
trans.commit()
