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

sentenceEmbedder = se()



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

    return [[arg_model, ml_arg], [claim_model, ml_claim], [premise_model, ml_premise]]
all_models = load_models()

def run_models(sentence):
    ## calculate eloquence
    errors = fe.find_sentence_errors(sentence)
    # argumentation
    ## non-argument: 0, claim: 1, premise: 2
    a_model = all_models[0][0]
    ml_arg = all_models[0][1]
    a_f = sentenceEmbedder.encode_one(sentence, ml_arg)
    a_label = a_model.predict(a_f)[0]

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
        # p_label: [logos, pathos, evidence, relevance, ethos]
        return {
            "content": sentence,
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
    temp = json.loads(request.data.decode("utf-8"))
    print("receive: ", temp)
    sentence = temp["input"]
    results = run_models(sentence)
    print("results:", results)
    return results






 

 




