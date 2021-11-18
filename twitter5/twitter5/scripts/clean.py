import re
import urllib
from numpy.lib.function_base import delete
import requests
import pandas as pd
import numpy as np
import time

#Natural language processing tool-kit
import nltk           
from nltk.corpus import stopwords

from sklearn.feature_extraction.text import CountVectorizer, ENGLISH_STOP_WORDS

# from main import get_hashtags_from_file

#Wordcloud imports
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image
import matplotlib.pyplot as plt
# nltk.download("stopwords")


class Clean:
    def __init__(self, df):
        self.df = self.__clean(df)

    def __clean(self, df):
        print('\nStart cleaning the dataframe...')
        start = time.time()

        df['hashtags'] = ''

        df.drop_duplicates(subset=["id"],inplace=True)

        new_tweets = []

        for index, tweet in df.iterrows():

            if tweet.language in ['en', 'es', 'de']:
                if tweet.language == 'en':
                    lang = 'english'
                if tweet.language == 'es':
                    lang = 'spanish'
                if tweet.language == 'de':
                    lang = 'german'

                hashtags = ''.join(j + ' ' for j in [i for i in tweet.text.split() if i.startswith('#')])

                stop_words = self.__get_stopwords(lang)
                stemmer = self.__get_stemmer(lang)
                tweet.text = self.__clean_text(tweet.text, stop_words, stemmer)
                tweet.hashtags = hashtags
                new_tweets.append(list(tweet))

        cleaned_df = pd.DataFrame(new_tweets, columns=[col for col in df])

        # Remove empty reviews
        cleaned_df = cleaned_df.loc[lambda x: x['text'] != '']

        # Drop duplicates after cleaning
        cleaned_df.drop_duplicates(subset=["text"],inplace=True)
        cleaned_df.geo_location = cleaned_df.geo_location.apply(lambda x: re.sub(r'[0-9]+', '', x))

        cleaned_df.reset_index(inplace=True, drop=True)

        end = time.time()
        print(f'Finished cleaning the dataframe in {end-start} seconds')
        return cleaned_df

    def __clean_text(self, text, stop_words, stemmer):
        whitelist = set('abcdefghijklmnopqrstuvwxyz# ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        clean_text = text.replace("<br>", " ")
        clean_text = clean_text.replace("\n", " ")
        clean_text = clean_text.encode('ascii', 'ignore').decode('ascii')
        clean_text = ''.join(i + ' ' for i in clean_text.split() if not i.startswith('http') and not i.startswith('@'))
        clean_text = ''.join(i + ' ' for i in [stemmer.stem(word) for word in clean_text.lower().split() if word not in stop_words])
        return ''.join(filter(whitelist.__contains__, clean_text))

    def __get_stopwords(self, language):
        """
        Cobine nltk's and hotel reviews specific stopwords and returns these as a set
        """
        stop_words = stopwords.words(language)
        return list(set(stop_words))

    def __get_stemmer(self, language):
        stemmer = nltk.stem.SnowballStemmer(language, ignore_stopwords=True)
        return stemmer
        