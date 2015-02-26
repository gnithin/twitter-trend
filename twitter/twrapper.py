#!/usr/bin/env python
import base64
import json
import pprint
import constants
import twitter_constants as t_const
import urllib
from req import https_req

def log(s):
    """
    Used to print to screen.
    Can be controlled to be turned off as well.
    """
    print(s)

class twrapper:
    def __init__(self, key, secret, screen_name):
        self.__key = key
        self.__secret = secret
        self.__https_obj = https_req(t_const.DOMAIN_NAME)
        self.screen_name = screen_name
        token = self.__authenticate()
        #raise Invalid creds exception here.
        if token == None:
            raise Exception("Cannot authenticate key and secret!")
        else:
            self.__token = token

    def set_screen_name(self, screen_name):
        self.screen_name = screen_name

    def get_screen_name(self):
        return self.screen_name
        
    def __authenticate(self):
        '''
        Used to auntheticate. Consumer key and secret are
        pre-defined. Returns the header if succesful else
        exits.
        '''
        #Acquiring the access token
        request_method = "POST"
        uri = t_const.URI_ACCESS_TOKEN
        param = urllib.urlencode({'grant_type':'client_credentials'})

        CONSUMER_KEY = self.__key
        CONSUMER_SECRET = self.__secret
        
        enc_str= base64.b64encode(CONSUMER_KEY+":"+CONSUMER_SECRET)
        headers = {"Authorization":"Basic "+enc_str,
                   "Content-type": "application/x-www-form-urlencoded;charset=UTF-8"}
        
        payload = self.__https_obj._make_req(uri, request_method, param, headers)
        if payload == None:
            log("Authentication Failed.")
            return None
        
        #Response type is always json
        #ref - https://dev.twitter.com/oauth/reference/post/oauth2/token
        try:
            dic = json.loads(payload)
        except ValueError:
            log("Authentication response Invalid.")
            return None
        if "errors" in dic or "access_token" not in dic:
            log("Error in authentication")
            return None
        
        access_token = dic.get("access_token")
        get_headers={"Authorization":"Bearer "+access_token}
        return get_headers

    def __get_tweets_from_json(self, json_data):
        """
        Takes a list
        and returns a list of tweet objects
        """
        tweets = list()
        list_of_tweets = json.loads(json_data)
        for t in list_of_tweets:
            tweets.append(tweet(t))
        return tweets

    def get_tweets(self, tweet_count):
        api_url = t_const.API_GET_TWEETS + "?screen_name=%s&count=%s"
        json_tweets = self.__https_obj._make_req(api_url % (self.screen_name, tweet_count),"GET", "", self.__token)
        if json_tweets == None:
            log("Error in receiving data")
            return None
        tweets = self.__get_tweets_from_json(json_tweets)
        return tweets

    def __del__(self):
        #Closing the connection.
        self.__https_obj.close()
        

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
        log("Screen Name: " + self._get_screen_name())
        log("Tweet: " + self._get_tweet())
        log("Retweets: " + str(self._get_retweets()))
        log("URLs: " + ", ".join(self._get_urls()))

# Test
if __name__ == "__main__":
    screen_name = "abshk11"
    #Testing with bad secret
    #twrapper_obj = twrapper(constants.CONSUMER_KEY, "asa", screen_name)
    #Ideally needs to be used with try catch block.
    twrapper_obj = twrapper(constants.CONSUMER_KEY, constants.CONSUMER_SECRET, screen_name)

    tweets = twrapper_obj.get_tweets(3)
    for t in tweets:
        t._print_details()
        log("----------------------------------")
    #Fetching tweets from another user.
    twrapper_obj.set_screen_name("Persie_Official")
    tweets = twrapper_obj.get_tweets(5)
    for t in tweets:
        t._print_details()
        log("----------------------------------")
    
    '''
    # use authenticate to get the token
    token = authenticate()

    # create a twitter obj with screen_name
    tc = twitter("abshk11")
    tc._set_conn()
    # Use the auth token and no of counts of tweets
    # for the screen_name(symantec)
    tweets = get_tweets_from_json(tc._fetch_tweets(token, 3))

    for t in tweets:
        print t._print_details()
        print "----------------------------------"
    '''

