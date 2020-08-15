'''
    The RESTful style api server
'''
from flask import render_template
from flask import Flask, request, redirect, jsonify, send_from_directory, make_response
from flask_cors import *
from server import app
from functools import wraps
import hashlib
import random
import time
import datetime
import os
import json
import requests
import subprocess
from math import sqrt

# app = Flask(__name__)
# CORS(app, supports_credentials=True)

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
    print(request)
    return "get input!"
    # if len(request.data) == 0:
    #     return json.dumps("null")
    # else:
    #     inputResult = request.data
    #     print(inputResult)
    #     return json.dumps(inputResult)


# @app.route('/uploadInput', methods=['POST'])
# def post_route():
#     if request.method == 'POST':
#         headers = request.headers
#         data = request.get_json()
#         print'headers:',headers
#         print('Data Received: "{data}"'.format(data=data))
#         return "Request Processed.\n"

# if __name__ == "__main__":
#     app.run()


 

 




