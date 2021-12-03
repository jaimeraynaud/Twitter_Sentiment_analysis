from numpy import MachAr
import requests
import os
import tweepy
import pandas as pd
import time
import datetime

import urllib.request, urllib.parse, urllib.error,urllib.request,urllib.error,urllib.parse,json,re,datetime,sys,http.cookiejar
from pyquery import PyQuery

class TwitterApi:
    
    def __init__(self):
        self.base_url = os.getenv('TWITTER_API_URL')
        self.api = self.__setup()

    def __setup(self):
        '''Seting up the twitter api'''
        consumer_key = os.getenv('TWITTER_KEY')
        consumer_secret = os.getenv('TWITTER_SECRET_SECRET_KEY')
        access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        return tweepy.API(auth)

    def get_hashtags(self, hashtags, locations):

        #Max Tweets the function retrieves
        MAX_TWEETS = 10
        twlist = []
        try:
            #Loops through every hashtag, for every hashtag there is an API call done to retrieve the tweets from that
            #specific hashtag
            for geo, country in locations:
                print('getting:', country)
                for hashtag in hashtags:
                    print('getting:', hashtag)
                    tweets = tweepy.Cursor(self.api.search_tweets,
                                    q=f'{hashtag} -filter:retweets', geocode= geo,
                                    tweet_mode='extended').items(MAX_TWEETS)
                    twlistap = [[tweet.id, tweet.full_text, tweet.lang, tweet.created_at, tweet.user.id, tweet.user.location, country] for tweet in tweets]
                    twlist.extend(twlistap)
        except Exception as e:
            print(e)
        
        print(twlist)
        print('finished')

        return pd.DataFrame(data=twlist, columns=['id', 'text', 'language', 'created_at', 'user_id', 'user_location', 'geo_location'])        

    def digital_ocean(self, geo, country, hashtag):
        MAX_TWEETS = 3000
        tweets = tweepy.Cursor(
            self.api.search_tweets,
            q=f'{hashtag} -filter:retweets', geocode=geo,
            tweet_mode='extended').items(MAX_TWEETS)
        tweets_data = [[tweet.id, tweet.full_text, tweet.lang, tweet.created_at, tweet.user.id, tweet.user.location, country] for tweet in tweets]
        return pd.DataFrame(data=tweets_data, columns=['id', 'text', 'language', 'created_at', 'user_id', 'user_location', 'geo_location'])

    def get_id(self, id):
        headers = {
            'Authorization': f'Bearer {self.token}',
        }

        return requests.get(self.base_url + str(id), headers=headers).text