#!/usr/bin/env python

# ld-commits.py: backend for LD commits

from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/')
def landing():
    return 'LD-commits server here, listening to your POST commit HTTP requests :-)'

@app.route('/', methods=['POST'])
def post_hook():
    push = json.loads(request.data)
    for c in push['commits']:
        print c['message']

    return push

if __name__ == '__main__':
    app.run(port=5000, debug=True)
