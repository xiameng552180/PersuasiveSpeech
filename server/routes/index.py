'''
    The RESTful style api server
'''
from flask import render_template
from flask import Flask, request, redirect, jsonify, send_from_directory, make_response
from flask_cors import *
from server import app
from functools import wraps
import pandas as pd
import hashlib
import random
import time
import datetime
import os
import json
import requests
import subprocess
from math import sqrt
from server.dataprocessing.sentenceCls import SentenceEmbedder as se
from server.dataprocessing import featureExtractor as fe
import torch
import transformers as ppb 
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import MultinomialNB, GaussianNB
from sklearn.neighbors import KNeighborsClassifier
import re
import numpy as np
sentenceEmbedder = se()

import sklearn
print("Sklearn verion is {}".format(sklearn.__version__))

import joblib


def load_models():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    # argument model
    with open(os.path.join(dir_path, "../models/argument_model.joblib"), 'rb') as f:
        arg_model = joblib.load(f)

    with open(os.path.join(dir_path, "../models/ml_argument.joblib"), 'rb') as f:
        ml_arg = joblib.load(f)

    # claim type model
    with open(os.path.join(dir_path, "../models/claim_model.joblib"), 'rb') as f:
        claim_model = joblib.load(f)

    with open(os.path.join(dir_path, "../models/ml_claims.joblib"), 'rb') as f:
        ml_claim = joblib.load(f)

    # premise type model
    with open(os.path.join(dir_path, "../models/premise_model.joblib"), 'rb') as f:
        premise_model = joblib.load(f)

    with open(os.path.join(dir_path, "../models/ml_premises.joblib"), 'rb') as f:
        ml_premise = joblib.load(f)

    # relationship model
    with open(os.path.join(dir_path, "../models/relations_mnodel.joblib"), 'rb') as f:
        relation_model = joblib.load(f)

    with open(os.path.join(dir_path, "../models/relation_len.joblib"), 'rb') as f:
        relation_len = joblib.load(f)

    
    return [[arg_model, ml_arg], [claim_model, ml_claim], [premise_model, ml_premise], [relation_model, relation_len]]
all_models = load_models()

def run_models(sentence):
    ## calculate eloquence
    errors = fe.find_sentence_errors(sentence)
    try:
        # print("query labels:", all_models)
        # argumentation
        ## non-argument: 0, claim: 1, premise: 2
        a_model = all_models[0][0]
        ml_arg = all_models[0][1]
        a_f = sentenceEmbedder.encode_one(sentence, ml_arg)
        a_label = a_model.predict(a_f)[0]
        print("prediction results:", a_model.predict(a_f))

        if a_label == 0:
            return {
                "content": sentence,
                "is_claim": 0,
                "claim_type": "0",
                "logos": 0,
                "pathos": 0,
                "evidence": 0,
                "relevance": 0,
                "ethos": 0,
                "concreteness": -1,
                "eloquence": errors[0],
                "elo_info": errors,
            }
        elif a_label == 1:
            # claim_type model
            c_model = all_models[1][0]
            ml_claim = all_models[1][1]
            c_f = sentenceEmbedder.encode_one(sentence, ml_claim)
            c_label = c_model.predict(c_f)[0]
            print("prediction results claim type:", c_model.predict(c_f))
            # interpretation: 1, evaluation: 2, disagreement/agreement: 0
            # convert to claim_type
            claim_type = "0"
            if c_label == 1:
                claim_type = "interpretation"
            elif c_label == 2:
                claim_type = "evaluation"
            else:
                claim_type = "disagreement"
            return {
                "content": sentence,
                "is_claim": 1,
                "claim_type": claim_type,
                "logos": 0,
                "pathos": 0,
                "evidence": 0,
                "relevance": 0,
                "ethos": 0,
                "concreteness": -1,
                "eloquence": errors[0],
                "elo_info": errors,
            }
        elif a_label == 2:
            p_model = all_models[2][0]
            ml_premise = all_models[2][1]
            p_f = sentenceEmbedder.encode_one(sentence, ml_premise)
            p_label = p_model.predict(p_f)[0]
            print("prediction results premises:", p_model.predict(p_f))
            # p_label: [logos, pathos, evidence, relevance, ethos]
            return {
                "content": sentence, #+ " .",
                "is_claim": 0,
                "claim_type": "0",
                "logos": int(p_label[0]),
                "pathos": int(p_label[1]),
                "evidence": int(p_label[2]),
                "relevance": int(p_label[3]),
                "ethos": int(p_label[4]),
                "concreteness": -1,
                "eloquence": int(errors[0]),
                "elo_info": errors,
            }
    
    except Exception as e:
        print("---model issues---")
        print(e)
        return {
            "content": sentence, #+ " .",
            "is_claim": 0,
            "claim_type": "0",
            "logos": 0,
            "pathos": 0,
            "evidence": 0,
            "relevance": 0,
            "ethos": 0,
            "concreteness": -1,
            "eloquence": int(errors[0]),
            "elo_info": errors,
        }


def run_relationship(sentences):
    # sentence relationship only computed when there are more than two sentences
    if len(sentences) >= 2:
        claims = []
        claim_id = []
        supports = []
        support_id = []
        for senid, sentence in enumerate(sentences):
            is_claim = sentence["is_claim"]
            # add claims
            if is_claim == 1:
                claims.append(sentence["content"])
                claim_id.append(senid)
            # add premises
            if sentence["logos"] + sentence["pathos"] + sentence["evidence"] + sentence["relevance"] + sentence["ethos"] >0:
                supports.append(sentence["content"])
                support_id.append(senid)
        # claim-support-pairs
        cspairs = []
        final_pairs = []
        ### HARCODE: if no claim, then 1st sentence will be the claim
        if len(claim_id) == 0:
            claim_id = [0]
        ###
        if len(claim_id) > 0 and len(support_id) > 0:
            for cid in claim_id:
                for sid in support_id:
                    if cid != sid: # claim != premise/supports
                        cspairs.append([cid, sid])
            #
            # print(cspairs)
            # if not empty, run relationship
            rmodel = all_models[3][0]
            rmodel_len = all_models[3][1]
            senEm = []
            for spair in cspairs:
                sen0 = sentences[spair[0]]["content"]
                sen1 = sentences[spair[1]]["content"]
                em0 = sentenceEmbedder.encode_one(sen0, rmodel_len)
                em1 = sentenceEmbedder.encode_one(sen1, rmodel_len)
                em = em0.tolist()[0] + em1.tolist()[0]
                senEm.append(em)
            # run pretrained model
            relation_scores = rmodel.predict(senEm)
            reidxs = np.where(relation_scores == 0)
            final_pairs = [cspairs[reidx] for reidx in reidxs[0]]

            # print("relationship score:",relation_scores, np.where(relation_scores == 0))
        
        # print("final pairs:", final_pairs)
        print("relationship pairs", final_pairs)
        return final_pairs
    else:
        return []

    


# run_models("hello")
# exit()

# app = Flask(__name__)
# CORS(app, supports_credentials=True)

@app.route('/')
def index():
    return render_template('index.html')


@app.route("/test", methods=['POST','GET'])
def register():
    print('hello world!')
    return 'get your request!'


@app.route('/uploadInput', methods=['POST','GET']) 
def uploadInput():

    response = json.loads(request.data.decode("utf-8"))
    txt = response["input"]["content"]
    userid = response["input"]["userid"]
    

    ### TODO: add more splitting operations
    # sentence_list = [s.strip() for s in re.split(r'[\.\?\!]+', txt) if len(s.strip()) > 0]
    sen_idxs = [m.start() for m in re.finditer(r'[\.\?\!]+', txt)]
    ini_idx = 0
    all_results = []

    for idx in sen_idxs:
        sen_txt = txt[ini_idx: idx+1]
        ini_idx = idx + 1
        if len(sen_txt.strip()) > 0:
            results = run_models(sen_txt)
            all_results.append(results)

    ### OLD one: have BUG
    # pattern = r'\.|/|\'|`|\[|\]|<|>|\?|:|\{|\}|\~|!||\(|\)|-|=|\_|、|；|‘|’|【|】|·|…'
    # pattern = r'\.|/|\'|`|\[|\]|<|>|\?|:|\{|\}|\~|!||\(|\)|-|=|\_|、|；|‘|’|【|】|·|…'
    # sentence_list = re.split(pattern, txt)
    # for index_sentence in range(0, len(sentence_list)-1): # split re without the last one
    #     results = run_models(sentence_list[index_sentence])
    #     all_results.append(results)

    # run relation models
    relationship_pairs = run_relationship(all_results)
    print("all_results:", all_results)
    print("relationship_pairs:", relationship_pairs)

    # save results
    dir_path = os.path.dirname(os.path.realpath(__file__))
    user_results_name = userid + str(time.time()) + ".json"
    with open(os.path.join(dir_path, "../dataset/user_inputs/"+user_results_name), "w") as f:
        json.dump({
        "results": all_results,
        "relationships": relationship_pairs}, f)
        
    return json.dumps({
        "results": all_results,
        "relationships": relationship_pairs
    })
