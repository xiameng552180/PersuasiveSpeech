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
    temp = json.dumps(request.data.decode("utf-8"))
        
    return temp






 

 




