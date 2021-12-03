import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, KFold, GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_curve, roc_auc_score
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelBinarizer



class ClassificationModel:
    def __init__(self, df, model, X='text', y='label', test_size=0.2, k_fold=None, plot_auc=False, vec='count', max_features=10000, ngram_range=(1,2)):
        self.df = df
        self.model = model
        self.X = X
        self.y = y
        self.test_size = test_size
        self.k_fold = k_fold
        self.plot_auc = plot_auc
        self.vec = self.__get_vecorizer(vec, max_features, ngram_range)

    def __get_vecorizer(self, vec, max_features, ngram_range):
        if vec == 'tfid':
            return self.__tfidf_vectorize(max_features, ngram_range)
        elif vec == 'count':
            return self.__count_vectorize(max_features, ngram_range)
        else:
            return self.__count_vectorize(max_features, ngram_range)

    def __count_vectorize(self, max_features, ngram_range):
        print('\nCreating CountVectorizer...')
        vec = CountVectorizer(ngram_range=ngram_range, max_features=max_features)
        vec = vec.fit(self.df[self.X].tolist())    
        return vec

    def __tfidf_vectorize(self, max_features, ngram_range):
        print('\nCreating TfidfVectorizer...')
        vec = TfidfVectorizer(ngram_range=ngram_range, max_features=max_features) 
        vec = vec.fit(self.df[self.X].tolist())    
        return vec

    def __create_matrix_df(self):
        wordcount = self.vec.transform(self.df[self.X].tolist())
        tokens = self.vec.get_feature_names_out()
        doc_names = ['Doc{:d}'.format(idx) for idx, _ in enumerate(wordcount)]
        return pd.DataFrame(data=wordcount.toarray(), index=doc_names, columns=tokens)

    def grid_search(self, params):
        print('\nGetting best parameters...')
        start = time.time()

        sc = StandardScaler()
        pipe = Pipeline(steps=[('sc', sc),('model', self.model)])
        grid_search = GridSearchCV(pipe, params, cv=5)
        grid_search.fit(self.__create_matrix_df(), self.df[self.y])

        end = time.time()

        print(f'Finished getting parameters in {end - start} seconds')
        print(f'Best score: {grid_search.best_score_}')
        print(f'Best parameters: {grid_search.best_estimator_.get_params()["model"]}')

        return grid_search

    def create_model(self):
        print(f'\nCreating model: {self.model}...')

        start = time.time()
        y = self.df[self.y]
        y = y.factorize()[0]
        X = self.__create_matrix_df()
        print(y)

        if not self.k_fold:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=self.test_size)

            self.model.fit(X_train, y_train)

            end = time.time()
            print(f'Finished creating {self.model} in {end - start} seconds')

            print('\nPredicting test data...')
            y_pred = self.model.predict(X_test)
            score = accuracy_score(y_test, y_pred)

            print(f'Score:', score)
            print(f'Confusion Matrix:\n', confusion_matrix(y_test, y_pred))
            print(f'Classification Report:\n', classification_report(y_test, y_pred))

        else:
            acc_score = []
            k_fold = KFold(n_splits=self.k_fold)

            for train_index, test_index in k_fold.split(X):
                start_time = time.time()
                X_train , X_test = X.iloc[train_index,:],X.iloc[test_index,:]
                y_train , y_test = y[train_index] , y[test_index]
                
                self.model.fit(X_train,y_train)
                y_pred = self.model.predict(X_test)
                
                acc = accuracy_score(y_pred , y_test)
                acc_score.append(acc)
                end_time = time.time()
                print(f'Finished creating {self.model} in {end_time - start_time} seconds')

            avg_acc_score = np.mean(acc_score)
            end = time.time()

            print(f'Finished creating all models in {end - start} seconds')

            print(f'All scores: {acc_score}')
            print(f'Avarage score: {avg_acc_score}')
            print(f'Confusion Matrix:\n', confusion_matrix(y_test, y_pred))
            print(f'Classification Report:\n', classification_report(y_test, y_pred))

        if self.plot_auc:
            y_pred_prob = self.model.predict_proba(X_test)[:, 1]

            fpr, tpr, thresholds = roc_curve(y_test, y_pred_prob)
            auc_score = roc_auc_score(y_test, y_pred_prob)

            plt.plot(fpr, tpr)
            plt.xlim([0.0, 1.0])
            plt.ylim([0.0, 1.0])
            plt.rcParams['font.size'] = 12
            plt.title(f'ROC curve for reviews (AUC: {auc_score})')
            plt.xlabel('False Positive Rate (1 - Specificity)')
            plt.ylabel('True Positive Rate (Sensitivity)')
            plt.grid(True)

            # from mlxtend.plotting import plot_decision_regions
            # plot_decision_regions(X_test.values, y_test.values, clf = self.model, legend = 2)

        return self


def create_basic_models(df, pickle=False):
    model = ClassificationModel(df, model=MultinomialNB(), vec='tfid', plot_auc = False)
    model.create_model()
    if pickle:
        pickle.dump(model.model, open('models/test_model.pickle', 'wb'))
        pickle.dump(model.vector, open('models/test_vec.pickle', 'wb'))

    model = ClassificationModel(df, model=LogisticRegression(), vec='tfid')
    model.create_model()
    if pickle:
        pickle.dump(model.model, open('models/logistic_regression_model.pickle', 'wb'))
        pickle.dump(model.vec, open('models/logistic_regression_vec.pickle', 'wb'))

    model = ClassificationModel(df, model=KNeighborsClassifier())
    model.create_model()
    if pickle:
        pickle.dump(model.model, open('models/knn_model.pickle', 'wb'))
        pickle.dump(model.vec, open('models/knn_vec.pickle', 'wb'))

    model = ClassificationModel(df, model=RandomForestClassifier(), vec='tfid')
    model.create_model()
    if pickle:
        pickle.dump(model.model, open('models/random_forest_model.pickle', 'wb'))
        pickle.dump(model.vec, open('models/random_forest_vec.pickle', 'wb'))

def logstic_regression(df):
    model = ClassificationModel(df, model=LogisticRegression(solver='liblinear'), k_fold=5, vec='tfid')

    best_params = model.grid_search({
        'model__penalty': ['l1','l2'], 
        'model__C': np.logspace(-4, 4, 50)
    })

    C = best_params.best_estimator_.get_params()['model__C']
    penalty = best_params.best_estimator_.get_params()['model__penalty']
    print(f'Best C:', C)
    print(f'Best Penalty:', penalty)
    model.model.C = C
    model.model.penalty = penalty

    logistic = model.create_model()

    return logistic

def random_forest(df):
    model = ClassificationModel(df, model=RandomForestClassifier(), k_fold=5, vec='tfid')

    best_params = model.grid_search({
        'model__n_estimators': list(range(30,121,10)), 
        'model__max_features': list(range(3,19,5))
    })

    n_estimators = best_params.best_estimator_.get_params()['model__n_estimators']
    max_features = best_params.best_estimator_.get_params()['model__max_features']
    print(f'Best n_estimators:', n_estimators)
    print(f'Best max_features:', max_features)
    model.model.n_estimators = n_estimators
    model.model.max_features = max_features

    forest = model.create_model()

    return forest
