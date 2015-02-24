#!/usr/bin/env python
import base64
import json
import ast
import pprint
import constants

#Imports that will fail in 3+
try:
    import httplib
except ImportError:
    import http.client as httplib

import urllib

### UTILS ###

class https_req:
    def __init__(self, domain):
        """
        TODO:
        Need to make this work for Python 3+
        """
        try:
            self._conn = httplib.HTTPSConnection(domain)
        except:
            self._conn = None
    
    def _get_conn(self):
        """
        Returns connection object.
        """
        return self._conn

    def _make_req(self, uri, request_method, params, headers):
        """
        Performs request and returns payload.
        Returns None if unsuccessful.
        Note: This does not close the connection upon exit.
        TODO:
        Need to make this work for Python 3+
        """
        try:
            self._conn.request(request_method, uri, params, headers)
            response=self._conn.getresponse()
        except:
            print "Error while performing https request."
            return None
        else:
            payload = response.read()
            return payload

    def _close_conn(self):
        """
        Closes connection.
        """
        if self._conn != None:
            self._conn.close()

def make_https_req(domain, uri, request_method, params, headers):
    """
    Performs https requests on the given params.
    Returns payload if success, None if request failed.
    """
    
    conn = get_https_conn(domain)
    if conn == None:
        return None
    payload = make_https_req(conn, uri, request_method, params, headers)
    conn.close()
    return payload

def authenticate():
    '''
    Used to auntheticate. Consumer key and secret are
    pre-defined. Returns the header if succesful else
    exits.
    '''    
    #Acquiring the access token
    domain_name = "api.twitter.com"
    request_method = "POST"
    uri = "/oauth2/token/"    
    param = urllib.urlencode({'grant_type':'client_credentials'})
    
    CONSUMER_KEY=constants.CONSUMER_KEY
    CONSUMER_SECRET=constants.CONSUMER_SECRET
    enc_str= base64.b64encode(CONSUMER_KEY+":"+CONSUMER_SECRET)
    headers = {"Authorization":"Basic "+enc_str,
               "Content-type": "application/x-www-form-urlencoded;charset=UTF-8"}
    
    https_obj = https_req(domain_name)
    payload = https_obj._make_req(uri, request_method, param, headers)
    
    if payload == None:
        print "Authentication Failed."
        return None
    
    ## Converting the payload string to a dictionary
    #dic = ast.literal_eval(payload)
    #Response type is always json
    #ref - https://dev.twitter.com/oauth/reference/post/oauth2/token
    try:
        dic = json.loads(payload)
    except ValueError:
        print "Authentication response Invalid."
        return None
    
    access_token = dic.get("access_token")
    get_headers={"Authorization":"Bearer "+access_token}
    return get_headers


def get_tweets_from_json(json_data):
    """
    Takes a list
    and returns a list of tweet objects
    """
    tweets = list()
    list_of_tweets = json.loads(json_data)

    for t in list_of_tweets:
        tweets.append(tweet(t))

    return tweets

##################################### END UTILS ########################################


class twitter():

    def __init__(self, screename, conn=None):
        """
        Expects the screen_name for which, the tweets will
        be fetched.
        """
        self._screename = screename
        self._conn = conn

    def _set_conn(self):
        """
        Sets the HTTP Connection with twitter api end point.
        Close the connection, when usage is done
        """
        self._conn = https_req("api.twitter.com")
        return self._conn

    def _close_conn():
        if conn:
            self._conn.close()

    def _fetch_tweets(self,authentication_token, counts):
        """
        Fetches <count> no. of tweets.
        Loads it into json and returns the json object.
        """
        api_url = "/1.1/statuses/user_timeline.json?screen_name=%s&count=%s"
        data_received = self._conn._make_req(api_url % (self._screename, counts),"GET", "", authentication_token)
        if data_received == None:
            print "Error in receiving data"
        return data_received

# add all the attributes as properties
# will make it more efficient
# shouldn't calculate if things have
# been calculated once
class tweet():
    def __init__(self, json_data):
        """
        Initialize the object with the tweet data(json)
        """
        self._tweet = json_data

    def _get_user(self):
        """
        Returns a dict with user details.
        Eg followers, location, screen_name etc
        """
        return self._tweet['user']

    def _get_screen_name(self):
        """
        Method to give the screen name for the tweet
        """
        user = self._get_user()
        return user['screen_name']

    def _get_location(self):
        """
        Returns location of the user
        """
        return self._get_user()['location']

    def _get_retweets(self):
        """
        Gives the count of retweets
        """
        return int(self._tweet['retweet_count'])

    def _get_tweet(self):
        """
        Gives the tweet. Could be a link or text
        """
        return self._tweet['text']

    def _get_urls(self):
        """
        Returns usable URLs (list o f URLs).
        The URLS can be directly used by urllib etc
        """
        usable_urls = list()
        urls = self._tweet['entities']['urls']

        for url in urls:
            usable_url = url['expanded_url']
            usable_url = usable_url.replace(" ","") # trimming
            usable_urls.append(usable_url)

        return usable_urls

    def _print_details(self):
        """
        Print the properties(not yet props)
        """
        print "Screen Name: " + self._get_screen_name()
        print "Tweet: " + self._get_tweet()
        print "Retweets: " + str(self._get_retweets())
        print "URLs: " + ", ".join(self._get_urls())

# Test
if __name__ == "__main__":
    # use authenticate to get the token
    token = authenticate()
    # create a twitter obj with screen_name
    
    tc = twitter("abshk11")
    tc._set_conn()
    # Use the auth token and no of counts of tweets
    # for the screen_name(symantec)
    tweets = get_tweets_from_json(tc._fetch_tweets(token, 3))

    for t in tweets:
        t._print_details()
        print "----------------------------------"
    
