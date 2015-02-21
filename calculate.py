#!/usr/bin/env python

"""
calculates time-zone contribution for each trending topic
"""

# Copyright (C) 2015  Abhishek Bhattacharjee <abhishek.bhattacharjee11@gmail.com>

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


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
