from dotenv import load_dotenv
import numpy as np
import requests

from scripts.twitter import TwitterApi
from scripts.database import DataBase
from scripts.unhcr import Unhcr
from scripts.clean import Clean
from scripts.words import graph, display_wordcloud
from scripts.classification_model import ClassificationModel, create_basic_models, test, random_forest
from scripts.tryout.tr import t
from scripts.cluster import cluster
from Oscar.dashapp.app import dashboard
def get_hashtags_from_file():
    with open('./files/hashtags.txt') as f:
        content = [line.split('\n')[0] for line in f.readlines()]
    return content

def get_locations_from_file():
    with open('./files/locations.txt') as f:
        content = [line.split('\n')[0].split(';') for line in f.readlines()]
    return content

def get_sentiment(analyzer, texts):
    texts = texts.apply(lambda x: str(analyzer.polarity_scores(x)))
    return texts

def print_labels(df):
    print(df.label.value_counts()/13066)
    for i in range(18):
        print(i)
        print(df[df['cluster'] == i].label.value_counts())

def print_words(df):
    graph(df[(df.sentiment_neu > 0.5)], len=50, name='Neutral Tweats (>0.5)')
    graph(df[(df.sentiment_pos > 0.2)], len=50, name='Positive Tweats (>0.2)')
    graph(df[(df.sentiment_neg > 0.2)], len=50, name='Negative Tweats (>0.2)')

def do_sentiment(df, threshold=0.05):
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    import json

    analyzer = SentimentIntensityAnalyzer()
    df['sentiment'] = get_sentiment(analyzer, df['text'])
    df['sentiment_neg'] = df['sentiment'].apply(lambda x: json.loads(x.replace("'",'"'))['neg'])
    df['sentiment_neu'] = df['sentiment'].apply(lambda x: json.loads(x.replace("'",'"'))['neu'])
    df['sentiment_pos'] = df['sentiment'].apply(lambda x: json.loads(x.replace("'",'"'))['pos'])
    df['sentiment_compound'] = df['sentiment'].apply(lambda x: json.loads(x.replace("'",'"'))['compound'])
    df.drop('sentiment', axis=1, inplace=True)
    # df['sentiment'] = ''
    df['label'] = 'neu'
    df.loc[(df.sentiment_compound > threshold), 'label'] = 'pos'
    df.loc[(df.sentiment_compound < -1*threshold), 'label'] = 'neg'
    return df

def new_tweets(df):
    # Clean: rewrite the clean for new languages
    clean = Clean(df)
    df = clean.df
    
    # Do Sentiment on the data
    df = do_sentiment(df)

    # Cluster the tweets
    # df = cluster(df)
    
    # db.upload_data(df, 'finalTweets', error='extend')

    return df

def __init__():
    load_dotenv()
    twitter = TwitterApi()
    unhcr = Unhcr()
    db = DataBase('tweets')
    return twitter, unhcr, db


if __name__ == "__main__":
    # RUN CODE HERE
    twitter, unhcr, db = __init__()
    df = db.get_tweets()
    # dashboard(df)
    # df = df[df['language']=='en']
    # df = new_tweets(df)
    # print(df)
    # print(df.cluster.value_counts())
    # print(df[df['language']=='en'])
    # print(Clean(df).df)
    # df = db.get_tweets()

    #df = df[df['language'] == 'en']
    # create_basic_models(df)
    #twitter_api(twitter, db)

    # create_basic_models(df)
    
    # df = df.drop('cluster',axiss=1)
    random_forest(df)

    # df = do_sentiment(df)

    # print(df.geo_location.value_counts())
    # print(df.label.value_counts())

    # db.upload_data(df, 'finalTweets', error='append')

