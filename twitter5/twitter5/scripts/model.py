import time

import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier

from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report


class Model:
    
    def __init__(self):

        # init the vectorizers
        self.countVectorizer = CountVectorizer(ngram_range=(1, 2), max_features=10000)
        self.tfVectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=15000)


    def countVector(self, df):

        # Create the count vectorizer
        vector = self.countVectorizer.fit(df.text)

        # Create the bag of words
        X = vector.transform(df.text)

        # Create and return the df
        X_df = pd.DataFrame(X.toarray(), columns=vector.get_feature_names_out())
        return X_df


    def tfidfVector(self, df):

        # Create the tfidf vectorizer
        vector = self.tfVectorizer.fit(df['text'].values.astype('U'))

        # Create the sparse matrix
        X = vector.transform(df['text'].values.astype('U'))

        # Create and return the df
        X_df = pd.DataFrame(X.toarray(), columns=vector.get_feature_names_out())
        return X_df


    def k_means(self, df, vector):

        # Start time
        beginTime = time.time()

        # Define label and X
        X = self.countVector(df)

        # Perform the train-test split
        #X_train, X_test, y_train, y_test = train_test_split(X, y, train_size = 0.75, test_size=0.25, random_state=0)

        # Build a the KMeans cluster model
        # n_clusters for how many clusters, in our case we want only 2, positive or negative towards refugees
        # n_init is how many times the algoritm is run with different centroid seeds, default 8
        # max_iter is how many itterations in a run, default 300
        # algoritm is the used algoritm, default auto, full is better
        cluster = []
        for i in range (1,11):
            model = KMeans(n_clusters=i, n_init=100, max_iter=1000, algorithm='full', random_state=0).fit(X)
            cluster.append(model.inertia_)

        plt.plot(range(1,11), cluster)
        plt.title('The Elbow Method')
        plt.xlabel('number of clusters')
        plt.ylabel('results')
        plt.show()

        print(model.labels_)
        print(model.cluster_centers_)
        print(model.n_iter_)
        print(model.inertia_)
        print(model.n_features_in_)
        print(model.feature_names_in_)

        Kmodel = KMeans().fit(X)
        clf = GridSearchCV(Kmodel, ["n_clusters=5", "n_init=100", "max_iter=1000", "algorithm='full'", "random_state=0"])
        clf.fit(X)

        # Create the prediction and print the results
        # y_predicted = model.predict(X_test)
        # print('[K Means] Accuracy score test set: ', accuracy_score(y_test, y_predicted))
        # print('[K Means] Confusion matrix test set: \n', confusion_matrix(y_test, y_predicted))
        # print('[K Means] Confusion matrix test set: \n', confusion_matrix(y_test, y_predicted)/len(y_test))
        # print(classification_report(y_test, y_predicted, target_names=['Racist', 'Not Racist']))

        # Calculate the time the regression took
        endTime = time.time()
        print("K Means duration: " + str(round(endTime - beginTime)) + " seconds")

        # Return the build model
        return model

    
    # def random_forest(self, df, vector):

    #     # Start time
    #     beginTime = time.time()

    #     # Create the count or tfidf vectorizer
    #     X_df, vector = self.countVector(df)
    #     #X_df, vector = self.tfidfVector(df)

    #     # Define label and X
    #     y = df['label']
    #     X = X_df

    #     # Perform the train-test split
    #     X_train, X_test, y_train, y_test = train_test_split(X, y, train_size = 0.75, test_size=0.25, random_state=0)

    #     # Build a random forest model and print out the accuracy
    #     #model = RandomForestClassifier(, max_depth=1000, n_jobs=-1).fit(X_train, y_train)
    #     model = RandomForestClassifier(n_estimators=500, min_samples_split=4, min_samples_leaf=2).fit(X_train, y_train)
    #     y_predicted = model.predict(X_test)
    #     print('[Random Forest] Accuracy score test set: ', accuracy_score(y_test, y_predicted))
    #     print('[Random Forest] Confusion matrix test set: \n', confusion_matrix(y_test, y_predicted)/len(y_test))
    #     print(classification_report(y_test, y_predicted, target_names=['Negatieve Review', 'Positieve Review']))

    #     # Calculate the time the random forest took
    #     endTime = time.time()
    #     print("Random Forest Duration: " + str(round(endTime - beginTime)) + " seconds")

    #     # Return the build model
    #     return model