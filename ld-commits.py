#!/usr/bin/env python

# ld-commits.py: backend for LD commits

from flask import Flask, request, jsonify
import json
from rdflib import Graph
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)-15s [%(levelname)s] (%(module)s.%(funcName)s) %(message)s')
logger = logging.getLogger(__name__)

@app.route('/')
def landing():
    return 'LD-commits server here, listening to your POST commit HTTP requests :-)'

@app.route('/', methods=['POST'])
def post_hook():
    push = json.loads(request.data)
    for c in push['commits']:
        commit_message = c['message']
    logger.debug('Received commit message: {}'.format(commit_message))
    # We'll ignore the first line of the commit message
    # Typically this line is by humans for humans
    
    logger.debug('Parsing triples from commit message')
    g = Graph()
    g.parse(data=commit_message, format='turtle')
    logger.debug('RDF graph parsed {} triples'.format(len(g)))
    
    return c['message']

if __name__ == '__main__':
    app.run(port=5000, debug=True)
