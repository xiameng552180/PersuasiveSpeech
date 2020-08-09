import numpy as np
import pandas as pd
import math
import torch

import transformers as ppb # pytorch transformers
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
# load models
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import MultinomialNB, GaussianNB
from sklearn.neighbors import KNeighborsClassifier
# load test data
from sklearn import datasets
from sklearn.metrics import classification_report



df = pd.read_csv('samples/train.tsv', delimiter='\t', header=None)[:2000]
print(df.head())

class ModelSelector(object):
    def __init__(self, data, labels):
        self.model_names = [
            "Linear SVM", "RBF SVM", "Logistic Regression", "Random Forest", "Multinomial Naive Bayes",
            "Gaussian NB", "Nearest Neighbor", "AdaBoosted Decision Tree",
        ]
        self.data = data
        self.label = labels
        self.models = [
            SVC(kernel = "linear", random_state=0),
            SVC(kernel='rbf', random_state=0),
            LogisticRegression(random_state=0),
            RandomForestClassifier(random_state=0),
            MultinomialNB(),
            GaussianNB(),
            KNeighborsClassifier(),
            AdaBoostClassifier(random_state=0),
        ]
        self.hyperparams = [
            {'kernel': ['linear'], 'C': [1e-2, 1e-1, 1, 10, 100, 1000]}, # linear svm
            {'kernel': ['rbf'], 'C': [1e-2, 1e-1, 1, 10, 100, 1000], "gamma":[1e-1, 1e-2, 1e-3, 1e-4]}, # rbf svm
            {"C":np.logspace(-3,3,7), "penalty":["l1","l2"]}, # LR
            {
                'max_features': ['auto', 'sqrt', 'log2'],
                'max_depth' : [4,5,6,7,8],
                'criterion' :['gini', 'entropy']
            }, # RF
            {"alpha": [math.pow(10, -i) for i in range(0,11)]}, # M-NB
            {}, # G-NB
            {"n_neighbors": [i for i in range(1,11)]}, # NN
            {}, # adaboost tree
        ]
    def initialization(self):
        print("--- this is testing ---")
        digits = datasets.load_digits()
        self.X = digits.images.reshape((len(digits.images), -1))
        self.y = digits.target
    
    def gridSearches(self):
        print("--- model hyper-parameter grid search ---")
        for modelid, model in enumerate(self.models):
            print(modelid, model, self.hyperparams[modelid])
            clf_para = self.hyperparams[modelid]
            clf = GridSearchCV(model, clf_para)
            clf.fit(self.X, self.y)
            print("Best parameters set found on development set:")
            print()
            print(clf.best_params_)
            print()
            print("Detailed classification report:")
            print()
            print("The model is trained on the full development set.")
            print("The scores are computed on the full evaluation set.")
            print()
            y_true, y_pred = self.y, clf.predict(self.X)
            print(classification_report(y_true, y_pred))
            
        

MS = ModelSelector(df[0], df[1])
print(MS.initialization())
print(MS.gridSearches())
exit()


def argument_tagging(data, labels):
    # load pre-trained bert components
    model_class, tokenizer_class, pretrained_weights = (ppb.DistilBertModel, ppb.DistilBertTokenizer, 'distilbert-base-uncased')
    # load pretrained model/tokenizer
    tokenizer = tokenizer_class.from_pretrained(pretrained_weights)
    model = model_class.from_pretrained(pretrained_weights)
    tokenized = data.apply((lambda x: tokenizer.encode(x, add_special_tokens=True)))
    print(len(tokenized))
    # padding feature vectors to have the same length (default to the max length of the sentences)
    max_len = 0
    for i in tokenized.values:
        if len(i) > max_len:
            max_len = len(i)
    print("sentences max length: {}".format(max_len))

    padded = np.array([i + [0]*(max_len-len(i)) for i in tokenized.values])
    # print("padded shape: {}".format(np.array(padded).shape))

    attention_mask = np.where(padded != 0, 1, 0)
    # print("attention masks: {}".format(attention_mask.shape))

    input_ids = torch.tensor(padded)  
    attention_mask = torch.tensor(attention_mask)
    
    # get output of the last layer (from the pre-trained BERT)
    with torch.no_grad():
        last_hidden_states = model(input_ids, attention_mask=attention_mask)
    
    # get first token ([cls]) embedding for classification
    features = last_hidden_states[0][:,0,:].numpy()

    print("features shape: {}".format(features.shape))
    
    # training/test of models
    train_features, test_features, train_labels, test_labels = train_test_split(features, labels, random_state = 42)
    lr_clf = LogisticRegression()
    lr_clf.fit(train_features, train_labels)
    
    print("test score: {}".format(lr_clf.score(test_features, test_labels)))
    
if __name__ == '__main__':
    argument_tagging(df[0], df[1])