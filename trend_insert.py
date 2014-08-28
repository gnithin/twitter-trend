#!/usr/bin/env python
"""
Takes 100 tweets and puts it in the database
"""
# Copyright (C) 2013  Abhishek Bhattacharjee <abhishek.bhattacharjee11@gmail.com>

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

################################################################################

import urllib
import httplib
import base64
import json
import ast
import pprint as pp
from pymongo import MongoClient
from bson.objectid import ObjectId as objid
import pdb

def put_into_database(trendname,screename,text,loc=None):
    try:
        client = MongoClient('localhost', 27017)
        db = client.test_database
        screen_name = db.tests.find_one({"trend":trendname,"screename":screename,"text":text})
        if not(screen_name):
            if loc:
                db.try1.insert({"trend":trendname,"screename":screename,"text":text,"location":loc})
            else:
                db.try1.insert({"trend":trendname,"screename":screename,"text":text,"location":"Others"})
            print "-----****Gone into the database"

        else:
            print "------****Already present"
    except:
        print "database error"


def get_info_for_trends(x,count=None):
    #printing each trending topic/person etc
    print "\n-----------Tweets for :" + x['name'] + "--------------"
    print x['query']
    if  not(count):
        conn.request("GET","/1.1/search/tweets.json?q="+str(x['query']),"",get_headers)
    else:
        conn.request("GET","/1.1/search/tweets.json?q="+str(x['query'])+"&count=100","",get_headers)
    
    tweets_resp = conn.getresponse()
    tweets = tweets_resp.read()
    tweets_json = json.loads(str(tweets))
    i=1
    #print pp.pprint(tweets_json)
    for s in tweets_json['statuses']:
        #printing names of users and tweets for each trending topic 
        print str(i)+". " +s['user']['name'].encode('utf-8')
        print s['text'].encode('utf-8')
        location = s['user']['location']
        time_zone = s['user']['time_zone']
        place = s['place']
        #if location:
        #    put_into_database(x['name'],s['user']['screen_name'],s['text'],location)
        if time_zone:
            put_into_database(x['name'],s['user']['screen_name'],s['text'],time_zone)
        #elif place:
        #    put_into_database(x['name'],s['user']['screen_name'],s['text'],place)
        else:
            put_into_database(x['name'],s['user']['screen_name'],s['text'])
        i=i+1

CONSUMER_KEY='tI0bUJuctVgzA82wGYLiQ'
CONSUMER_SECRET='59GVWA6j7RJt1Ntw2cFi57FS91jzRFIk6lbNzH8Cs8'

#OAUTH_TOKEN='165807027-Y9GeHly2EiJ5LBzcI3eAGvNp9M44kpO5tK9yfu2n'
#OAUTH_TOKEN_SECRET='qTopfcbhvo1qo3RvWvqzxDg2IHeJETyz8x5SPn8n0zk'

enc_str= base64.b64encode(CONSUMER_KEY+":"+CONSUMER_SECRET)


if __name__ == "__main__":

    try:
        conn = httplib.HTTPSConnection("api.twitter.com")

        #Acquiring the access token
        param = urllib.urlencode({'grant_type':'client_credentials'})
        headers = {"Authorization":"Basic "+enc_str,
                   "Content-type": "application/x-www-form-urlencoded;charset=UTF-8"}
        

        conn.request("POST","/oauth2/token/",param,headers)
        response=conn.getresponse()
        payload = response.read()

        ##Converting the payload string to a dictionary
        dic = ast.literal_eval(payload)
        access_token = dic.get("access_token")

        get_headers={"Authorization":"Bearer "+access_token}
        
        ##Getting WorldWide Trends 
        conn.request("GET","/1.1/trends/place.json?id=1","",get_headers)  
        get_resp = conn.getresponse()
        sample = get_resp.read()
        
        ##converting the received string in JSON form 
        data = json.loads(str(sample))
        #print pp.pprint(data[0])
        names = data[0]['trends']
        
        print "-----------------------------Trends-----------------------------------"
        for x in names:
            try:
                get_info_for_trends(x,"100")
            except:
                try:
                    get_info_for_trends(x)
                except:
                    print "Error.... :( "
            
    except:
        print "something went wrong :("
            
    print "\n"

