import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
#import spacy
from sklearn.model_selection import train_test_split
import nltk
from nltk.tokenize import RegexpTokenizer, WhitespaceTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import string
from string import punctuation
import collections
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
#import en_core_web_sm
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import jaccard_score

def t(df):
    #print(df.info())
    df = df[df['language'] == 'en']
    #nlp = en_core_web_sm.load() 
    tokenizer = RegexpTokenizer(r'\w+')
    lemmatizer = WordNetLemmatizer()
    stop = set(stopwords.words('english'))
    punctuation = list(string.punctuation) #already taken care of with the cleaning function.
    stop.update(punctuation)
    w_tokenizer = WhitespaceTokenizer()

    def furnished(text):
        final_text = []
        for i in w_tokenizer.tokenize(text):
            if i.lower() not in stop:
                word = lemmatizer.lemmatize(i)
                final_text.append(word.lower())
        return  ' '.join(final_text)

    df.text = df.text.apply(furnished)
    pos_rel_list = [ 'help', 'support', 'like', 'need', 'thank', 'welcom', 'love', 'work', 'care', 'want', 'get', 'good', 'join', 'make', 'countri', 'new', 'great', 'would', 'asylum', 'look', 'live', 'famili', 'share', 'see', 'free', 'hope', 'come', 'well', 'go', 'take', 'right', 'way', 'children', 'mani', 'here', 'pleas', 'protect']
    neu_rel_list = ['us', 'peopl', 'help', 'need', 'support', 'like', 'get', 'welcom', 'countri', 'work', 'new', '#refuge', 'one', 'asylum', 'live', 'right', 'immigr', 'mani', 'come', 'take', 'uk', 'make', 'go', 'state', 'would', 'year', 'want', 'camp', 'resettl', 'children', 'border', 'famili', 'govern', 'say', 'home', 'afghanistan', 'world', 'see', 'know', 'time', 'look', 'today', 'refugee', 'hous', 'think', 'im']
    neg_rel_list = ['war', 'kill', 'rape', 'stop', 'govern', 'border', 'drown', 'murder', 'death', 'take', 'go', 'say', 'attack', 'camp', 'call', 'charg', 'montana', 'hate', 'biden', 'dont', 'back', 'world']
    
    def listToString(s): 
        # initialize an empty string
        str1 = "" 
        # traverse in the string  
        for ele in s: 
            str1 += ele   
        return str1

    positive_related_words = listToString(pos_rel_list)
    negative_related_words = listToString(neg_rel_list)
    positive = furnished(positive_related_words)
    negative = furnished(negative_related_words)

    string1 = positive
    words = string1.split()
    positive = " ".join(sorted(set(words), key=words.index))

    string1 = negative
    words = string1.split()
    negative = " ".join(sorted(set(words), key=words.index))

    def jaccard_similarity(query, document):
        intersection = set(query).intersection(set(document))
        union = set(query).union(set(document))
        return len(intersection)/len(union)

    def get_scores(group,tweets):
        scores = []
        for tweet in tweets:
            s = jaccard_similarity(group, tweet)
            scores.append(s)
        return scores

    pos_scores = get_scores(positive, df.text.to_list())
    neg_scores = get_scores(negative, df.text.to_list())

    # create a jaccard scored df.
    data  = {'names':df.user_id.to_list(), 'positive_score':pos_scores,
            'negative_score': neg_scores}
    scores_df = pd.DataFrame(data)
    #assign classes based on highest score
    def get_classes(l1, l2):
        pos = []
        neg = []

        for i, j in zip(l1, l2):
            m = max(i, j)
            if m == i:
                pos.append(1)
            else:
                pos.append(0)
            if m == j:
                neg.append(1)
            else:
                neg.append(0)           
                
        return pos, neg

    l1 = scores_df.positive_score.to_list()
    l2 = scores_df.negative_score.to_list()

    pos, neg = get_classes(l1, l2)
    data = {'name': scores_df.names.to_list(), 'positive':pos, 'negative':neg}
    class_df = pd.DataFrame(data)
    #grouping the tweets by username
    new_groups_df = class_df.groupby(['name']).sum()
    #add a new totals column
    new_groups_df['total'] = new_groups_df['positive'] + new_groups_df['negative']
    #add a new totals row
    new_groups_df.loc["Total"] = new_groups_df.sum()

    fig = plt.figure(figsize =(10, 7)) 
    a = new_groups_df.drop(['total'], axis = 1)
    plt.pie(a.loc['Total'], labels = a.columns)
    plt.title('A pie chart showing the volumes of tweets under different categories.')
    plt.show()

    X = new_groups_df[['positive', 'negative']].values
    X = X[:-1]
    print(X)
    # Elbow Method
    from sklearn.cluster import KMeans
    wcss = []
    for i in range(1, 11):
        kmeans = KMeans(n_clusters=i, init='k-means++', n_init=10, max_iter=300, random_state=0)
        kmeans.fit(X)
        wcss.append(kmeans.inertia_)
    plt.plot(range(1,11), wcss)
    plt.title('Elbow Method')
    plt.xlabel('Number of Clusters')
    plt.ylabel('wcss')
    plt.show()


    # fitting kmeans to dataset
    kmeans = KMeans(n_clusters=2, init='k-means++', n_init=10, max_iter=300, random_state=0)
    print(X)
    Y_kmeans = kmeans.fit_predict(X)
    print(Y_kmeans)
    # Visualising the clusters
    plt.scatter(X[Y_kmeans==0, 0], X[Y_kmeans==0, 1],  c='red', label= 'Cluster 1')
    plt.scatter(X[Y_kmeans==1, 0], X[Y_kmeans==1, 1],  c='green', label= 'Cluster 2')
    


    plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], c='black', label='Centroids' )
    plt.title('Clusters of tweets in positive and negative groups')
    plt.xlabel('positive tweets')
    plt.ylabel('negative tweets')
    plt.legend()
    plt.show()