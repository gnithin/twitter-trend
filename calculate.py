#!/usr/bin/env python

import json
import pprint as pp
from pymongo import MongoClient
from bson.objectid import ObjectId as objid
import pdb

client = MongoClient('localhost', 27017)
db = client.test_database
data = db.try1.find()
current_trend=[]
country=[]

trend_list=db.try1.distinct('trend')

i=0
while(i < len(trend_list)):
    data = db.try1.find({'trend':trend_list[i]})
    country.append({})
    for d in data:
        if country[i].get(d['location']):
            country[i][d['location']]+=1
        else:
            country[i][d['location']]=1
    i+=1

print "----------------Trends and time-zone wise contribution-------------"
i=0
while i < len(country):
    print "Trend: ",trend_list[i]
    for loc,count in country[i].iteritems():
        print loc," : ",count
    print "---------------------------------"
    i+=1
