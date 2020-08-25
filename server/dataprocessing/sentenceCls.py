import numpy as np
import os
import json
import pandas as pd
import math
from scipy import stats
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
from sklearn.metrics import classification_report, f1_score
from sklearn.multiclass import OneVsRestClassifier
print("Sklearn verion is {}".format(sklearn.__version__))
# save model
import joblib

import warnings
warnings.filterwarnings("ignore")

#### data folder configuration
dir_path = os.path.dirname(os.path.realpath(__file__))
new_dataset_folder = os.path.join(dir_path, '../dataset/posts_new/')

# "/data2/xingbo/chi2021/meng/PersuasiveSpeech/server/dataset/posts_new/"
models_path = os.path.join(dir_path, '../dataset/models/')
# "/data2/xingbo/chi2021/meng/PersuasiveSpeech/server/models/"
# df = pd.read_csv('samples/train.tsv', delimiter='\t', header=None)[:2000]
# # print(df.head())

def isNaN(num):
    return num != num

def isMultiLabel(arr):
    a = arr[0]
    try:
        if len(a) > 1:
            return True
        else:
            return False
    except Exception:
        return False

### load dataset and organize training/testing data
def load_dataset(input_folder):
    debates_files = os.listdir(input_folder)
    # argument data
    argument_data = []
    argument_label = []
    # claim type data
    claim_type_data = []
    claim_type_label = []
    # premise type data
    premise_type_data = []
    premise_type_label = []
    
    for debate_file in debates_files:
        if debate_file.endswith(".json"):
            with open(os.path.join(input_folder, debate_file), "r") as f:
                debate_data = json.load(f)
            # print(debate_file)
            for dkey in debate_data.keys():
                # argument data
                ## non-argument: 0, claim: 1, premise: 2
                argument_data.append(debate_data[dkey][0]["op_claim"])
                argument_label.append(1)
                
                replys = debate_data[dkey][0]["reply-info"]
                for reply in replys:
                    contents = reply["reply_contents"]
                    for content in contents:
                        # print(content.keys())
                        # exit()
                        # get sentence content
                        sentence = content["content"]
                        # get claim/premise, strategies
                        is_claim = int(content["is_claim"])
                        logos = int(content["logos"])
                        pathos = int(content["pathos"])
                        evidence = int(content["evidence"])
                        relevance = int(content["relevance"])
                        ethos = int(content["ethos"])
                        if isNaN(content["concreteness"]):
                            content["concreteness"] = 0
                        # print(sentence, is_claim, isNaN(content["concreteness"]))
                        
                        ## collect argument data
                        if is_claim == 0 and logos == 0 and pathos == 0 and evidence == 0 and relevance ==0 and ethos == 0:
                            argument_data.append(sentence)
                            argument_label.append(0)
                        else:
                            if is_claim == 1:
                                # argument data
                                argument_data.append(sentence)
                                argument_label.append(1)
                                # claim type
                                claim_type_data.append(sentence)
                                claim_type = content["claim_type"].lower()
                                if "interpretation" in claim_type:
                                    claim_type_label.append(1)
                                elif "evaluation" in claim_type:
                                    claim_type_label.append(2)
                                else:
                                    claim_type_label.append(0)
                            else:
                                argument_data.append(sentence)
                                argument_label.append(2)
                                # premise type
                                premise_type_data.append(sentence)
                                # logos, pathos, evidence, relevance, ethos
                                premise_type_label.append([logos, pathos, evidence, relevance, ethos])
                                
    # return argument, claim, premise
    return {"X": argument_data, "y": argument_label}, {"X": claim_type_data, "y": claim_type_label}, {"X": premise_type_data, "y": premise_type_label}
arguments, claims, premises = load_dataset(new_dataset_folder)
# print("total # of data:", len(premises["X"]))
# exit()

### model selector
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
            # {},
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
            # {"n_estimators": [10, 50, 100, 150, 200, 500, 1000], "learning_rate": [1, 1e-1, 1e-2, 1e-3, 1e-4]}, # adaboost tree
            {"n_estimators": [100], "learning_rate": [1, 1e-1, 1e-2, 1e-3, 1e-4]}, # adaboost tree
        ]
        self.hyperparams_ = [
            {'estimator__kernel': ['linear'], 'estimator__C': [1e-2, 1e-1, 1, 10, 100, 1000]}, # linear svm
            # {},
            {'estimator__kernel': ['rbf'], 'estimator__C': [1e-2, 1e-1, 1, 10, 100, 1000], "estimator__gamma":[1e-1, 1e-2, 1e-3, 1e-4]}, # rbf svm
            {"estimator__C":np.logspace(-3,3,7), "estimator__penalty":["l1","l2"]}, # LR
            {
                'estimator__max_features': ['auto', 'sqrt', 'log2'],
                'estimator__max_depth' : [4,5,6,7,8],
                'estimator__criterion' :['gini', 'entropy']
            }, # RF
            {"estimator__alpha": [math.pow(10, -i) for i in range(0,11)]}, # M-NB
            {}, # G-NB
            {"estimator__n_neighbors": [i for i in range(1,11)]}, # NN
            # {"n_estimators": [10, 50, 100, 150, 200, 500, 1000], "learning_rate": [1, 1e-1, 1e-2, 1e-3, 1e-4]}, # adaboost tree
            {"estimator__n_estimators": [100], "estimator__learning_rate": [1, 1e-1, 1e-2, 1e-3, 1e-4]}, # adaboost tree
        ]
    def initialization(self):
        print("--- this is testing ---")
        
        ## test case: digits dataset
        # digits = datasets.load_digits()
        # self.X = digits.images.reshape((len(digits.images), -1))
        # self.y = digits.target
        # self.X = self.data
        # self.y = self.label
        
        ## training/test of models
        train_features, test_features, train_labels, test_labels = train_test_split(self.data, self.label, test_size=0.2, random_state = 42)
        self.train_X = train_features
        self.train_y = train_labels
        self.test_X = test_features
        self.test_y = test_labels
        
        
        # print(stats.describe(self.y))
        # exit()
    
    def gridSearches(self):
        print("--- model hyper-parameter grid search ---")
        clfs = []
        clfs_name = []
        clf_acc = []
        ## tell whether multi-label or not 
        # print(self.train_y.to_numpy())
        # print(isMultiLabel(self.train_y.to_numpy()))
        # exit()
        flag = isMultiLabel(self.train_y.to_numpy())
        if flag:
            # prepare labels for multi-label classification
            self.train_y = np.array([np.array(ele) for ele in self.train_y.to_numpy()])
            self.test_y = np.array([np.array(ele) for ele in self.test_y.to_numpy()])
            
        for modelid, model in enumerate(self.models): 
            try:
                print(self.model_names[modelid])
                # print(modelid, self.model_names[modelid], self.hyperparams[modelid])
                clf_para = self.hyperparams[modelid]
                if flag:
                    model = OneVsRestClassifier(model)
                    clf_para = self.hyperparams_[modelid]            
                clf = GridSearchCV(model, clf_para)
                clf.fit(self.train_X, self.train_y)
                # print("Best parameters set found on development set:")
                # print()
                # print(clf.best_params_)
                print()
                print("Detailed classification report:")
                print()
                print("The model is trained on the full development set.")
                print("The scores are computed on the full evaluation set.")
                print()
                # y_true, y_pred = self.train_y, clf.predict(self.train_X)
                y_true, y_pred = self.test_y, clf.predict(self.test_X)
                # print(classification_report(y_true, y_pred))
                # print(balanced_accuracy_score(y_true, y_pred))
                clfs.append(clf)
                clfs_name.append(self.model_names[modelid])
                clf_acc.append(f1_score(y_true, y_pred, average='weighted'))
            except Exception:
                # print(self.model_names[modelid])
                # # print(modelid, self.model_names[modelid], self.hyperparams[modelid])
                # clf_para = self.hyperparams[modelid]
                # if isMultiLabel(self.train_y.to_numpy()):
                #     model = OneVsRestClassifier(model)
                #     clf_para = self.hyperparams_[modelid]            
                # clf = GridSearchCV(model, clf_para)
                # clf.fit(self.train_X, self.train_y)
                # # print("Best parameters set found on development set:")
                # # print()
                # # print(clf.best_params_)
                # print()
                # print("Detailed classification report:")
                # print()
                # print("The model is trained on the full development set.")
                # print("The scores are computed on the full evaluation set.")
                # print()
                # # y_true, y_pred = self.train_y, clf.predict(self.train_X)
                # y_true, y_pred = self.test_y, clf.predict(self.test_X)
                # print(f1_score(y_true, y_pred))
                continue
            # exit()
        # find maximum acc.
        print("acc. score:{}".format(clf_acc))
        bestidx = np.argmax(clf_acc)
        bestmodel = clfs[bestidx]
        print("best model: {}".format(clfs_name[bestidx]))
        return bestmodel
    
            
        

# MS = ModelSelector(arguments["X"], arguments["y"])
# print(MS.initialization())
# print(MS.gridSearches())
# exit()


### sentence feature extractor
class SentenceEmbedder(object):
    def __init__(self):
        model_class, tokenizer_class, pretrained_weights = (ppb.DistilBertModel, ppb.DistilBertTokenizer, 'distilbert-base-uncased')
        self.tokenizer = tokenizer_class.from_pretrained(pretrained_weights)
        self.model = model_class.from_pretrained(pretrained_weights)
        print("---sentence embedder initialization---")
    def encode(self, data, labels):
        tokenized = data.apply((lambda x: self.tokenizer.encode(x, add_special_tokens=True)))
        # print("encoding shape: {}".format(tokenized.shape))
        # padding feature vectors to have the same length (default to the max length of the sentences)
        max_len = 0
        for i in tokenized.values:
            if len(i) > max_len:
                max_len = len(i)
        print("sentences max length: {}".format(max_len))


        padded = np.array([i + [0]*(max_len-len(i)) for i in tokenized.values])
        
        attention_mask = np.where(padded != 0, 1, 0)
        # print("attention masks: {}".format(attention_mask.shape))

        input_ids = torch.tensor(padded)  
        attention_mask = torch.tensor(attention_mask)
        
        # get output of the last layer (from the pre-trained BERT)
        with torch.no_grad():
            last_hidden_states = self.model(input_ids, attention_mask=attention_mask)
        
        # get first token ([cls]) embedding for classification
        features = last_hidden_states[0][:,0,:].numpy()

        print("features shape: {}".format(features.shape))
        
        return features, max_len
    
    def encode_one(self, sentence, max_len):
        tokenized = self.tokenizer.encode(sentence, add_special_tokens=True)
        # print("encoding shape: {}".format(len(tokenized)))
        if max_len < len(tokenized):
            padded = tokenized[:max_len]
        else:
            padded = np.array([tokenized + [0]*(max_len-len(tokenized))])
        attention_mask = np.where(padded != 0, 1, 0)
        input_ids = torch.tensor(padded)  
        attention_mask = torch.tensor(attention_mask)
        with torch.no_grad():
            last_hidden_states = self.model(input_ids, attention_mask=attention_mask)
        features = last_hidden_states[0][:,0,:].numpy()
        return features
        
        
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
    

### predictor


if __name__ == '__main__':
    ## test case ONE
    # argument_tagging(df[0], df[1])
    
    ## test case TWO
    # arguments_df = pd.DataFrame(arguments)
    # argument_tagging(arguments_df["X"], arguments_df["y"])
    
    ## 
    # 1. argument data
    arguments_df = pd.DataFrame(arguments)
    argument_sentences = arguments_df["X"]
    argument_labels = arguments_df["y"]
    
    # 2. claim type data
    claim_df = pd.DataFrame(claims)
    claims_sentences = claim_df["X"]
    claims_labels = claim_df["y"]
    
    # 3. premises type data
    premises_df = pd.DataFrame(premises)
    premises_sentences = premises_df['X']
    premises_labels = premises_df["y"]
    
    # ## select argument models
    # sentenceEmbedder = SentenceEmbedder()
    # features, ml_argument = sentenceEmbedder.encode(argument_sentences, argument_labels)

    # # print(ml_argument)
    # # new_f = sentenceEmbedder.encode_one("hello", ml_argument)

    # MS = ModelSelector(features, argument_labels)    
    # MS.initialization()
    # best_argument_model = MS.gridSearches()

    # # print("predictions:", best_argument_model.predict(new_f))

    # ## save models & input size
    # with open(os.path.join(models_path, "argument_model.joblib"), 'wb') as f:
    #     joblib.dump(best_argument_model, f)
    
    # with open(os.path.join(models_path, "ml_argument.joblib"), 'wb') as f:
    #     joblib.dump(ml_argument, f)
    # print("--- save argument model ---")
    
    # # select claim_type models
    # sentenceEmbedder = SentenceEmbedder()
    # features, ml_claims = sentenceEmbedder.encode(claims_sentences, claims_labels)
    # MS = ModelSelector(features, claims_labels)    
    # MS.initialization()
    # best_claims_model = MS.gridSearches()

    # with open(os.path.join(models_path, "claim_model.joblib"), 'wb') as f:
    #     joblib.dump(best_claims_model, f)
    # with open(os.path.join(models_path, "ml_claims.joblib"), 'wb') as f:
    #     joblib.dump(ml_claims, f)
    # print("--- save claim model ---")

    # select premise_type models
    sentenceEmbedder = SentenceEmbedder()
    features, ml_premises = sentenceEmbedder.encode(premises_sentences, premises_labels)
    MS = ModelSelector(features, premises_labels)
    MS.initialization()
    best_premise_model = MS.gridSearches()

    with open(os.path.join(models_path, "premise_model.joblib"), 'wb') as f:
        joblib.dump(best_premise_model, f)
    with open(os.path.join(models_path, "ml_premises.joblib"), 'wb') as f:
        joblib.dump(ml_premises, f)
    print("--- save premise model ---")
    
    