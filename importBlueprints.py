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

industryBlueprints = Table('industryBlueprints',metadata,
							Column('typeID',Integer,primary_key=True, autoincrement=False),
							Column('maxProductionLimit',Integer)
							)
							
industryActivity = Table('industryActivity',metadata,
							Column('typeID',Integer,primary_key=True, autoincrement=False),
							Column('activityID',Integer,primary_key=True, autoincrement=False,index=True),
							Column('time',Integer)
							)


industryActivityMaterials = Table('industryActivityMaterials',metadata,
							Column('typeID',Integer,index=True),
							Column('activityID',Integer),
							Column('materialTypeID',Integer),
							Column('quantity',Integer)
							)

Index('industryActivityMaterials_idx1',industryActivityMaterials.c.typeID,industryActivityMaterials.c.activityID)

industryActivityProducts = Table('industryActivityProducts',metadata,
							Column('typeID',Integer,index=True),
							Column('activityID',Integer),
							Column('productTypeID',Integer,index=True),
							Column('quantity',Integer)
							)

Index('industryActivityProduct_idx1',industryActivityProducts.c.typeID,industryActivityProducts.c.activityID)

industryActivitySkills = Table('industryActivitySkills',metadata,
							Column('typeID',Integer,index=True),
							Column('activityID',Integer),
							Column('skillID',Integer,index=True),
							Column('level',Integer)
							)

Index('industryActivitySkills_idx1',industryActivitySkills.c.typeID,industryActivitySkills.c.activityID)

industryActivityProbabilities = Table('industryActivityProbabilities',metadata,
							Column('typeID',Integer,index=True),
							Column('activityID',Integer),
							Column('productTypeID',Integer,index=True),
							Column('probability',Numeric(scale=2,precision=3))
							)


metadata.create_all(engine,checkfirst=True)

activityIDs={"copying":5,"manufacturing":1,"research_material":4,"research_time":3,"invention":8};



print "opening Yaml"
with open('blueprints.yaml','r') as yamlstream:
    print "importing"
    trans = connection.begin()
    blueprints=yaml.load(yamlstream,Loader=yaml.CSafeLoader)
    print "Yaml Processed into memory"
    for blueprint in blueprints:
        connection.execute(industryBlueprints.insert(),typeID=blueprint,maxProductionLimit=blueprints[blueprint]["maxProductionLimit"])
        for activity in blueprints[blueprint]['activities']:
			connection.execute(industryActivity.insert(),
								typeID=blueprint,
								activityID=activityIDs[activity],
								time=blueprints[blueprint]['activities'][activity]['time'])
			if blueprints[blueprint]['activities'][activity].has_key('materials'):
				for material in blueprints[blueprint]['activities'][activity]['materials']:
					connection.execute(industryActivityMaterials.insert(),
										typeID=blueprint,
										activityID=activityIDs[activity],
										materialTypeID=material['typeID'],
										quantity=material['quantity'])
			if blueprints[blueprint]['activities'][activity].has_key('products'):
				for product in blueprints[blueprint]['activities'][activity]['products']:
					connection.execute(industryActivityProducts.insert(),
										typeID=blueprint,
										activityID=activityIDs[activity],
										productTypeID=product['typeID'],
										quantity=product['quantity'])
					if product.has_key('probability'):
						connection.execute(industryActivityProbabilities.insert(),
											typeID=blueprint,
											activityID=activityIDs[activity],
											productTypeID=product['typeID'],
											probability=product['probability'])
			if blueprints[blueprint]['activities'][activity].has_key('skills'):
				for skill in blueprints[blueprint]['activities'][activity]['skills']:
					connection.execute(industryActivitySkills.insert(),
										typeID=blueprint,
										activityID=activityIDs[activity],
										skillID=skill['typeID'],
										level=skill['level'])
				
trans.commit()
